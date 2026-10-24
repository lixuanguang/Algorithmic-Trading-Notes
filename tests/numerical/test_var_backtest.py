"""Tests of the VaR backtest's simulation, window timing, violation masks and statistics.

The example's full run is tested in test_checks.py. These pin down the GARCH-t recursion and
its draws, that day t's VaR uses only the window before it and FHS scales by day t's own
variance, the strict violation comparison, LR_uc against an independent form and its
existing limits, and the clustering conditions, with small inputs or prepared masks.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import contextlib
import io
import math
import unittest
from unittest import mock

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical import var_backtest as vb
from trading_notes.numerical.report import CheckReport


def path(returns: list[float], variances: list[float]) -> vb.GarchPath:
    """Return a prepared path."""
    return vb.GarchPath(np.array(returns), np.array(variances))


def hits(*days: int) -> NDArray[np.bool_]:
    """Return a violation mask of the given 0s and 1s."""
    return np.array(days, dtype=np.bool_)


class Simulation(unittest.TestCase):
    """Unit-variance t(6) shocks drawn at once; the variance recursion from its long-run level."""

    def test_recursion_and_draws(self) -> None:
        """sigma2_0 = omega / (1 - a - b); r_t = sigma_t z_t; sigma2_{t+1} from r_t and sigma2_t."""
        with mock.patch.object(vb, "DAYS", 5):
            rng = np.random.default_rng(vb.SEED)
            got = vb.simulate_garch_t(rng)
        replay = np.random.default_rng(vb.SEED)
        z = replay.standard_t(6, 5) / math.sqrt(1.5)
        s2 = [1e-6 / (1 - 0.08 - 0.90)]
        r = []
        for t in range(5):
            r.append(math.sqrt(s2[t]) * z[t])
            s2.append(1e-6 + 0.08 * r[t] ** 2 + 0.90 * s2[t])
        np.testing.assert_array_equal(got.returns, r)
        np.testing.assert_array_equal(got.variances, s2[:5])
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)


class Backtest(unittest.TestCase):
    """Day t's VaR comes from days t - window to t - 1; a violation is strictly below -VaR."""

    def test_current_return_is_excluded(self) -> None:
        """At p = 0 the HS VaR is minus the window's minimum, so only an excluded r_t can breach it.

        Were r_t in its own window, it could never lie strictly below that window's minimum.
        """
        got = vb.backtest(path([0.0, 0.0, 0.0, 0.0, -1.0], [1.0] * 5), window=4, p=0.0)
        np.testing.assert_array_equal(got.hs, hits(1))
        np.testing.assert_array_equal(got.fhs, hits(1))

    def test_violation_is_strict(self) -> None:
        """A return equal to -VaR is not a violation."""
        got = vb.backtest(path([-1.0, 0.0, 0.0, 0.0, -1.0], [1.0] * 5), window=4, p=0.0)
        np.testing.assert_array_equal(got.hs, hits(0))
        np.testing.assert_array_equal(got.fhs, hits(0))

    def test_fhs_scales_by_the_current_variance(self) -> None:
        """Residual quantile -1 times day t's sigma 3 gives VaR 3; HS's VaR is 2.

        A return of -2.5 breaches HS only. With the previous day's sigma of 2, FHS's VaR
        would also be 2 and it would be breached too.
        """
        prepared = path([-2.0, 2.0, -2.0, 2.0, -2.5], [4.0, 4.0, 4.0, 4.0, 9.0])
        got = vb.backtest(prepared, window=4, p=0.0)
        np.testing.assert_array_equal(got.hs, hits(1))
        np.testing.assert_array_equal(got.fhs, hits(0))

    def test_masks_cover_each_day_after_the_first_window(self) -> None:
        """One boolean per day from `window` on, in day order, the two methods kept apart."""
        returns = [-2.0, 2.0, -2.0, 2.0, -2.5, -0.5, -3.5]
        variances = [4.0, 4.0, 4.0, 4.0, 9.0, 0.25, 4.0]
        got = vb.backtest(path(returns, variances), window=4, p=0.0)
        self.assertEqual((got.hs.dtype, got.fhs.dtype), (np.bool_, np.bool_))
        # Day 5: HS VaR 2.5; FHS residual minimum -1 times sigma 0.5 gives 0.5, breached
        # only by a return below -0.5. Day 6: HS VaR 2.5 is breached; FHS's window holds the
        # residuals -1, 1, -2.5/3 and -1, so its VaR is 2.
        np.testing.assert_array_equal(got.hs, hits(1, 0, 1))
        np.testing.assert_array_equal(got.fhs, hits(0, 0, 1))


class Statistics(unittest.TestCase):
    """LR_uc and the conditional violation rate."""

    def test_lr_uc_matches_twice_t_times_divergence(self) -> None:
        """LR_uc = 2 T [pi ln(pi/p) + (1 - pi) ln((1 - pi)/(1 - p))], pi = T1 / T."""
        h = hits(*([1] * 3 + [0] * 97))
        pi, p = 0.03, 0.01
        kl = pi * math.log(pi / p) + (1 - pi) * math.log((1 - pi) / (1 - p))
        self.assertAlmostEqual(vb.lr_uc(h, p), 2 * 100 * kl, places=12)
        self.assertAlmostEqual(vb.lr_uc(hits(*([1] + [0] * 99)), 0.01), 0.0, places=12)

    def test_lr_uc_limits_are_unchanged(self) -> None:
        """With no violations, or all, a log of zero still raises; nothing is clipped."""
        for h in (hits(0, 0, 0), hits(1, 1, 1)):
            with self.subTest(h=h.tolist()), self.assertRaises(ValueError):
                vb.lr_uc(h, 0.01)

    def test_rate_after_violation(self) -> None:
        """Only the days after a violation count, here days 1, 2 and 4: one of three."""
        self.assertEqual(vb.rate_after_violation(hits(1, 1, 0, 1, 0)), 1 / 3)


def clustered(k: int) -> NDArray[np.bool_]:
    """Return a mask with 25 violations, k of them on the day after another one."""
    return hits(*[1] * (k + 1), 0, *[1, 0] * (24 - k))


class Conditions(unittest.TestCase):
    """HS must exceed 4 percent; FHS must be strictly under half of HS."""

    def failures(self, hs: NDArray[np.bool_], fhs: NDArray[np.bool_]) -> list[str]:
        """Return the clustering failures for prepared masks."""
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            vb.check_clustering(report, vb.Violations(hs, fhs))
        return report.failures

    def test_edges(self) -> None:
        """At exactly 4 percent after a violation, or exactly half of HS, a condition fails."""
        self.assertEqual(
            [vb.rate_after_violation(clustered(k)) for k in (0, 1, 2)], [0, 0.04, 0.08]
        )
        self.assertEqual(self.failures(clustered(2), clustered(0)), [])
        self.assertEqual(self.failures(clustered(1), clustered(0)), ["HS violations cluster"])
        self.assertEqual(
            self.failures(clustered(2), clustered(1)), ["FHS violations do not cluster as much"]
        )


if __name__ == "__main__":
    unittest.main()
