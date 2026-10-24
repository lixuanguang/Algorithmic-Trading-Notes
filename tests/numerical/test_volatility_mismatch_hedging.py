"""Tests of the volatility-mismatch simulation's common paths and draw order.

The example's full run is tested in test_checks.py. These pin down, on a few short paths, that
all four hedges share one Brownian path per run (common random numbers), drawn as one normal
vector per fine step, and that the coarse grid rebalances on every tenth fine date.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import contextlib
import unittest
from unittest import mock

# third party library imports
import numpy as np

# project library imports
from trading_notes.numerical import volatility_mismatch_hedging as vm

SMALL = {"N_PATHS": 4, "N_FINE": 20}


def small_run(seed: int, **patches: float) -> tuple[vm.Simulation, np.random.Generator]:
    """Return a short simulation and its generator afterwards."""
    rng = np.random.default_rng(seed)
    with contextlib.ExitStack() as stack:
        for name, value in (SMALL | patches).items():
            stack.enter_context(mock.patch.object(vm, name, value))
        return vm.simulate(rng, vm.price(vm.S0, vm.T, vm.SIG_I)), rng


class CommonPaths(unittest.TestCase):
    """One path drives every hedge; only the hedging volatility and grid differ."""

    def test_equal_volatilities_give_equal_hedges(self) -> None:
        """With implied = actual, the 'a' and 'i' hedges coincide and the integral is zero."""
        sim, _ = small_run(7, SIG_I=vm.SIG_A)
        for grid in ("fine", "coarse"):
            np.testing.assert_array_equal(sim.pnl[(grid, "a")], sim.pnl[(grid, "i")])
            np.testing.assert_array_equal(sim.integral[grid], np.zeros(SMALL["N_PATHS"]))
        self.assertEqual(
            list(sim.pnl), [("fine", "a"), ("fine", "i"), ("coarse", "a"), ("coarse", "i")]
        )

    def test_draws_one_vector_per_fine_step(self) -> None:
        """The generator advances by exactly N_FINE vectors of N_PATHS normals."""
        _, rng = small_run(11)
        replay = np.random.default_rng(11)
        for _ in range(SMALL["N_FINE"]):
            replay.standard_normal(SMALL["N_PATHS"])
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)

    def test_coarse_grid_uses_every_tenth_date(self) -> None:
        """At COARSE_EVERY = N_FINE the coarse hedge keeps its initial delta to expiry.

        Its P&L is then the static hedge's, recomputed here from the same terminal prices.
        """
        sim, _ = small_run(3, COARSE_EVERY=SMALL["N_FINE"])
        rng = np.random.default_rng(3)
        dt = vm.T / SMALL["N_FINE"]
        S = np.full(SMALL["N_PATHS"], vm.S0)
        for _ in range(SMALL["N_FINE"]):
            S = S * np.exp(
                (vm.MU - vm.SIG_A**2 / 2) * dt
                + vm.SIG_A * np.sqrt(dt) * rng.standard_normal(SMALL["N_PATHS"])
            )
        Vi = vm.price(vm.S0, vm.T, vm.SIG_I)
        for hedge_vol, vol in (("a", vm.SIG_A), ("i", vm.SIG_I)):
            d0 = vm.delta(vm.S0, vm.T, vol)
            cash = (-Vi + d0 * vm.S0) * np.exp(vm.R * dt) ** SMALL["N_FINE"]
            want = np.exp(-vm.R * vm.T) * (np.maximum(S - vm.K, 0) - d0 * S + cash)
            np.testing.assert_allclose(sim.pnl[("coarse", hedge_vol)], want, rtol=1e-12)


if __name__ == "__main__":
    unittest.main()
