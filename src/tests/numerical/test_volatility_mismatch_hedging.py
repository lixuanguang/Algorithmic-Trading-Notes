"""Tests of the volatility-mismatch simulation's common paths and draw order."""

import unittest

import numpy as np

from trading_notes.numerical.option_hedging import volatility_mismatch_hedging_checks as vm
from trading_notes.numerical.option_hedging.volatility_mismatch import Simulation

SMALL = {"n_paths": 4, "n_fine": 20}


def small_run(seed: int, **changes: float) -> tuple[Simulation, np.random.Generator]:
    """Return a short simulation of the example with some inputs changed, and its generator."""
    rng = np.random.default_rng(seed)
    experiment = vm.EXPERIMENT.model_copy(update=SMALL | changes)
    Vi = vm.CALL.price(vm.S0, vm.T, experiment.implied_vol)
    return experiment.simulate(rng, Vi), rng


class CommonPaths(unittest.TestCase):
    """One path drives every hedge; only the hedging volatility and grid differ."""

    def test_equal_volatilities_give_equal_hedges(self) -> None:
        """With implied = actual, the 'a' and 'i' hedges coincide and the integral is zero."""
        sim, _ = small_run(7, implied_vol=vm.SIG_A)
        for grid in ("fine", "coarse"):
            np.testing.assert_array_equal(sim.pnl[(grid, "a")], sim.pnl[(grid, "i")])
            np.testing.assert_array_equal(sim.integral[grid], np.zeros(SMALL["n_paths"]))
        self.assertEqual(
            list(sim.pnl), [("fine", "a"), ("fine", "i"), ("coarse", "a"), ("coarse", "i")]
        )

    def test_draws_one_vector_per_fine_step(self) -> None:
        """The generator advances by exactly n_fine vectors of n_paths normals."""
        _, rng = small_run(11)
        replay = np.random.default_rng(11)
        for _ in range(SMALL["n_fine"]):
            replay.standard_normal(SMALL["n_paths"])
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)

    def test_coarse_grid_uses_every_tenth_date(self) -> None:
        """At coarse_every = n_fine the coarse hedge keeps its initial delta to expiry.

        Its P&L is then the static hedge's, recomputed here from the same terminal prices.
        """
        sim, _ = small_run(3, coarse_every=SMALL["n_fine"])
        rng = np.random.default_rng(3)
        dt = vm.T / SMALL["n_fine"]
        S = np.full(SMALL["n_paths"], vm.S0)
        for _ in range(SMALL["n_fine"]):
            S = S * np.exp(
                (vm.MU - vm.SIG_A**2 / 2) * dt
                + vm.SIG_A * np.sqrt(dt) * rng.standard_normal(SMALL["n_paths"])
            )
        Vi = vm.CALL.price(vm.S0, vm.T, vm.SIG_I)
        for hedge_vol, vol in (("a", vm.SIG_A), ("i", vm.SIG_I)):
            d0 = vm.CALL.delta(vm.S0, vm.T, vol)
            cash = (-Vi + d0 * vm.S0) * np.exp(vm.R * dt) ** SMALL["n_fine"]
            want = np.exp(-vm.R * vm.T) * (np.maximum(S - vm.K, 0) - d0 * S + cash)
            np.testing.assert_allclose(sim.pnl[("coarse", hedge_vol)], want, rtol=1e-12)


if __name__ == "__main__":
    unittest.main()
