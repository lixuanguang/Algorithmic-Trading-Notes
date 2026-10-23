"""Tests of the Cartea-Jaimungal demonstration: its sequences, its output and its routines.

The demonstration asserts nothing, so these tests do not give it a pass or fail contract. They
pin down the two seeded sequences, the shape of what a run prints and the computational
contracts of its routines, the latter with short computations rather than the run's own.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import contextlib
import io
import math
import random
import re
import unittest
from unittest import mock

# project library imports
from tests.numerical.test_checks import GlobalState, prime_global_random, restored_global_state
from trading_notes.numerical import cartea_jaimungal as cj

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
    "--- follow-up checks (#-#-#)",
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
        continued = cj.monte_carlo_variance(rng)
        reseeded = cj.monte_carlo_variance(random.Random(1))
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
            first = cj.monte_carlo_variance(rng, paths=50, steps=20)
            self.assertEqual(GlobalState.now(), before)
        replay = random.Random(9)
        for _ in range(50 * 20):
            replay.gauss(0, math.sqrt(1 / 20))
        self.assertEqual(rng.getstate(), replay.getstate())
        self.assertEqual(cj.monte_carlo_variance(random.Random(9), paths=50, steps=20), first)

    def test_monte_carlo_is_near_one_twentieth(self) -> None:
        """2000 paths estimate the variance 1/20 to within 0.005."""
        self.assertAlmostEqual(cj.monte_carlo_variance(random.Random(3), 2000), 0.05, delta=0.005)


class Riccati(unittest.TestCase):
    """The corrected closed form meets h2(T) = -A; the printed one gives A - b."""

    def test_terminal_values(self) -> None:
        """h2(T) = -xi(T) - b/2 is -A when corrected and A - b as printed."""
        k, phi, A, b, T = 0.01, 0.001, 0.5, 0.002, 1.0
        self.assertAlmostEqual(-cj.xi(T, T, k, phi, A, b) - b / 2, -A, places=12)
        self.assertAlmostEqual(-cj.xi(T, T, k, phi, A, b, printed=True) - b / 2, A - b, places=12)

    def test_almgren_chriss_limit(self) -> None:
        """With A very large the inventory follows sinh(gamma (T - t)) / sinh(gamma T)."""
        g = math.sqrt(0.001 / 0.01)
        quarter, half, end = cj.path(0.01, 0.001, 1e6, n=2000)
        self.assertAlmostEqual(quarter, math.sinh(g * 0.75) / math.sinh(g), places=3)
        self.assertAlmostEqual(half, math.sinh(g * 0.5) / math.sinh(g), places=3)
        self.assertEqual(end, 0.0)


class WealthAndFeedback(unittest.TestCase):
    """The simulation, the identity, the direct optimum and the feedback stay separate routes."""

    PARAMETERS = (1.0, 0.01, 0.001, 0.05, 0.02, 0.01, 1.0, 200)

    def test_identity_is_exact_without_trading(self) -> None:
        """With nu = 0 the Euler reward equals the identity up to rounding."""
        rng = random.Random(2)
        mu = [rng.uniform(-1, 1) for _ in range(400)]
        args = (1.0, 10.0, 0.1, 0.01, 0.02, 0.001, 0.08, 1.0)
        simulated, q_end = cj.wealth_sim([0.0] * 400, mu, *args)
        self.assertEqual(q_end, 1.0)
        with mock.patch.object(cj, "wealth_sim", side_effect=AssertionError):
            identity = cj.wealth_identity([0.0] * 400, mu, *args)
        self.assertAlmostEqual(simulated, identity, places=12)

    def test_printed_payoff_adds_half_the_spread(self) -> None:
        """The printed terminal payoff exceeds the corrected one by psi/2 Q_T."""
        nu, mu = [0.5] * 100, [0.0] * 100
        args = (1.0, 10.0, 0.1, 0.01, 0.02, 0.001, 0.08, 1.0)
        corrected, q_end = cj.wealth_sim(nu, mu, *args)
        printed, _ = cj.wealth_sim(nu, mu, *args, printed=True)
        self.assertAlmostEqual(printed - corrected, 0.02 / 2 * q_end, places=12)

    def test_direct_optimum_matches_feedback_independently(self) -> None:
        """The tridiagonal optimum uses no closed form, and both payoffs agree to 1e-3."""
        for printed in (False, True):
            with self.subTest(printed=printed):
                with mock.patch.object(cj, "xi", side_effect=AssertionError):
                    direct = cj.direct_optimum(*self.PARAMETERS, printed)
                with mock.patch.object(cj, "direct_optimum", side_effect=AssertionError):
                    feedback = cj.feedback_path(*self.PARAMETERS, printed)
                self.assertEqual(len(direct), len(feedback))
                self.assertAlmostEqual(direct[99], feedback[99], delta=1e-3)
                self.assertAlmostEqual(direct[-1], feedback[-1], delta=1e-3)

    def test_quadrature_converges_to_one_twentieth(self) -> None:
        """The midpoint rule's error falls by four when the grid doubles."""
        errors = [cj.quadrature_variance(m) - 1 / 20 for m in (50, 100)]
        self.assertAlmostEqual(errors[0] / errors[1], 4.0, places=3)
        self.assertLess(abs(errors[1]), 1e-5)


if __name__ == "__main__":
    unittest.main()
