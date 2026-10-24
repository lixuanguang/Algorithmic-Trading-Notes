"""Tests of the Cartea-Jaimungal demonstration: its sequences, its output and its routines."""

# The demonstration asserts nothing, so these tests do not give it a pass or fail contract. They
# pin down the two seeded sequences, the shape of what a run prints and the computational
# contracts of its routines, the latter with short computations rather than the run's own.

import contextlib
import io
import math
import random
import re
import unittest
from unittest import mock

from trading_notes.numerical.execution_control import cartea_jaimungal_checks as cj
from trading_notes.numerical.execution_control.optimal_liquidation import (
    LiquidationModel,
    monte_carlo_variance,
    quadrature_variance,
)

from .single_run import GlobalState, prime_global_random, restored_global_state

# What a run prints, with every number replaced by #.
SKELETON = [
    "HJB reduction difference -#",
    "HJB reduction difference #",
    "HJB reduction difference #",
    "h#(#): ODE -#, corrected form -#, printed form #",
    "h#(T) printed form # (should be -A = -#)",
    "h#(#): ODE #, b*FK #, boxed without b #",
    "Q at t = #, #, #",
    "  base kappa=# phi=# A=# [#, #, #]",
    "  phi x#                        [#, #, #]",
    "  A x#                          [#, #, #]",
    "  kappa x#                      [#, #, #]",
    "  A=#                          [#, #, #] Almgren-Chriss sinh [#, #]",
    "--- wealth identity, feedback policies and the unbounded counterexample",
    "wealth identity: simulated #, identity #",
    "corrected payoff: Q(T/#) direct # feedback #; Q(T) direct # feedback #",
    "printed   payoff: Q(T/#) direct # feedback #; Q(T) direct # feedback #",
    "nu = -M: M^# coefficient b/# - kappa - A - phi/# = #",
    "  M=   # reward #, reward/M^# #",
    "  M=  # reward #, reward/M^# #",
    "  M= # reward #, reward/M^# #",
    "  A=# > b/#: M=# reward/M^# -# (b/# - kappa - A - phi/# = -#)",
    "Var int (#-t) B_t dt: quadrature #, Monte Carlo #, #/# = #",
]
NUMBER = re.compile(r"\d+(?:\.\d+)?(?:e[+-]?\d+)?")


class SeededRun(unittest.TestCase):
    """One full run, made with the generator class observed."""

    out: str
    status: int
    seeds: list[tuple[object, ...]]

    @classmethod
    def setUpClass(cls) -> None:
        """Run the demonstration once, recording each generator it creates."""
        out = io.StringIO()
        with (
            restored_global_state(),
            mock.patch.object(random, "Random", wraps=random.Random) as made,
            contextlib.redirect_stdout(out),
        ):
            prime_global_random(5)
            cls.status = cj.main()
        cls.out = out.getvalue()
        cls.seeds = [c.args for c in made.call_args_list]

    def test_output_shape_and_status(self) -> None:
        """The run prints its 22 lines in order and returns 0."""
        self.assertEqual(self.status, 0)
        self.assertEqual([NUMBER.sub("#", line) for line in self.out.splitlines()], SKELETON)

    def test_two_generators_seeded_0_then_1(self) -> None:
        """Exactly two generators are made, seed 0 for the HJB lines and seed 1 for the rest."""
        self.assertEqual(self.seeds, [(0,), (1,)])

    def test_hjb_lines_come_from_seed_0(self) -> None:
        """The three HJB lines are those of a seed-0 generator's first 24 uniforms."""
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            cj.show_hjb_reduction(random.Random(0))
        self.assertTrue(self.out.startswith(printed.getvalue()))

    def test_monte_carlo_continues_the_seed_1_sequence(self) -> None:
        """The Monte Carlo draws follow the 8000 uniforms of nu and mu from the same generator."""
        rng = random.Random(1)
        for _ in range(2 * 4000):
            rng.uniform(0, 1)
        continued = monte_carlo_variance(rng)
        reseeded = monte_carlo_variance(random.Random(1))
        last = self.out.splitlines()[-1]
        self.assertIn(f"Monte Carlo {continued:.5f},", last)
        self.assertNotEqual(f"{continued:.5f}", f"{reseeded:.5f}")


class Generators(unittest.TestCase):
    """The Monte Carlo draws only from the generator it is given."""

    def test_monte_carlo_uses_its_generator_in_order(self) -> None:
        """It draws paths * steps Gaussians, in order, and leaves the shared state alone."""
        with restored_global_state():
            prime_global_random(6)
            before = GlobalState.now()
            rng = random.Random(9)
            first = monte_carlo_variance(rng, paths=50, steps=20)
            self.assertEqual(GlobalState.now(), before)
        replay = random.Random(9)
        for _ in range(50 * 20):
            replay.gauss(0, math.sqrt(1 / 20))
        self.assertEqual(rng.getstate(), replay.getstate())
        self.assertEqual(monte_carlo_variance(random.Random(9), paths=50, steps=20), first)

    def test_monte_carlo_is_near_one_twentieth(self) -> None:
        """2000 paths estimate the variance 1/20 to within 0.005."""
        self.assertAlmostEqual(monte_carlo_variance(random.Random(3), 2000), 0.05, delta=0.005)


class Riccati(unittest.TestCase):
    """The corrected closed form meets h2(T) = -A; the printed one gives A - b."""

    def test_terminal_values(self) -> None:
        """h2(T) = -xi(T) - b/2 is -A when corrected and A - b as printed."""
        A, b, T = 0.5, 0.002, 1.0
        model = LiquidationModel(kappa=0.01, phi=0.001, terminal=A, permanent=b, horizon=T)
        self.assertAlmostEqual(-model.xi(T) - b / 2, -A, places=12)
        self.assertAlmostEqual(-model.xi(T, printed=True) - b / 2, A - b, places=12)

    def test_almgren_chriss_limit(self) -> None:
        """With A very large the inventory follows sinh(gamma (T - t)) / sinh(gamma T)."""
        g = math.sqrt(0.001 / 0.01)
        quarter, half, end = LiquidationModel(kappa=0.01, phi=0.001, terminal=1e6).inventory(2000)
        self.assertAlmostEqual(quarter, math.sinh(g * 0.75) / math.sinh(g), places=3)
        self.assertAlmostEqual(half, math.sinh(g * 0.5) / math.sinh(g), places=3)
        self.assertEqual(end, 0.0)


class WealthAndFeedback(unittest.TestCase):
    """The simulation, the identity, the direct optimum and the feedback stay separate routes."""

    MODEL = LiquidationModel(kappa=0.01, phi=0.001, terminal=0.05, permanent=0.02, spread=0.01)
    # The wealth examples' model: b = 0.1, kappa = 0.01, psi = 0.02, phi = 0.001, A = 0.08.
    WEALTH = LiquidationModel(kappa=0.01, phi=0.001, terminal=0.08, permanent=0.1, spread=0.02)

    def test_identity_is_exact_without_trading(self) -> None:
        """With nu = 0 the Euler reward equals the identity up to rounding."""
        rng = random.Random(2)
        mu = [rng.uniform(-1, 1) for _ in range(400)]
        simulated, q_end = self.WEALTH.wealth([0.0] * 400, mu, 1.0, 10.0)
        self.assertEqual(q_end, 1.0)
        with mock.patch.object(LiquidationModel, "wealth", side_effect=AssertionError):
            identity = self.WEALTH.wealth_identity([0.0] * 400, mu, 1.0, 10.0)
        self.assertAlmostEqual(simulated, identity, places=12)

    def test_printed_payoff_adds_half_the_spread(self) -> None:
        """The printed terminal payoff exceeds the corrected one by psi/2 Q_T."""
        nu, mu = [0.5] * 100, [0.0] * 100
        corrected, q_end = self.WEALTH.wealth(nu, mu, 1.0, 10.0)
        printed, _ = self.WEALTH.wealth(nu, mu, 1.0, 10.0, printed=True)
        self.assertAlmostEqual(printed - corrected, 0.02 / 2 * q_end, places=12)

    def test_direct_optimum_matches_feedback_independently(self) -> None:
        """The tridiagonal optimum uses no closed form, and both payoffs agree to 1e-3."""
        for printed in (False, True):
            with self.subTest(printed=printed):
                with mock.patch.object(LiquidationModel, "xi", side_effect=AssertionError):
                    direct = self.MODEL.direct_optimum(1.0, 200, printed)
                with mock.patch.object(
                    LiquidationModel, "direct_optimum", side_effect=AssertionError
                ):
                    feedback = self.MODEL.feedback_path(1.0, 200, printed)
                self.assertEqual(len(direct), len(feedback))
                self.assertAlmostEqual(direct[99], feedback[99], delta=1e-3)
                self.assertAlmostEqual(direct[-1], feedback[-1], delta=1e-3)

    def test_quadrature_converges_to_one_twentieth(self) -> None:
        """The midpoint rule's error falls by four when the grid doubles."""
        errors = [quadrature_variance(m) - 1 / 20 for m in (50, 100)]
        self.assertAlmostEqual(errors[0] / errors[1], 4.0, places=3)
        self.assertLess(abs(errors[1]), 1e-5)


if __name__ == "__main__":
    unittest.main()
