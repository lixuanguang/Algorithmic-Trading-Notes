"""Tests of the dividend tree's date conventions and its exercise log.

The example's full run is tested in test_checks.py. These pin down which dividends the tree
counts (ex-dates up to and including maturity, none after it), that a European value depends
only on S* at maturity, and what the exercise log records.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import math
import unittest

# project library imports
from trading_notes.numerical import dividend_tree_swaption as dts

S0, K, R, SIG, T, STEPS = 50.0, 50.0, 0.05, 0.25, 0.5, 200


def tree(divs: list[tuple[float, float]], *, call: bool = True, american: bool = False) -> float:
    """Return the tree value at the module's test inputs."""
    return dts.dividend_tree(S0, K, R, SIG, T, STEPS, divs, call=call, american=american)


class DividendDates(unittest.TestCase):
    """A dividend counts if its ex-date is at or before maturity."""

    def test_dividend_after_maturity_is_ignored(self) -> None:
        """An ex-date after T leaves every value as without dividends, even American."""
        for american in (False, True):
            with self.subTest(american=american):
                self.assertEqual(
                    tree([(T + 0.01, 2.0)], american=american), tree([], american=american)
                )

    def test_european_value_depends_on_s_star_only(self) -> None:
        """A European call with a dividend D at t <= T is the call on S0 - D e^{-rt}."""
        for t_ex in (0.2, T):
            with self.subTest(t_ex=t_ex):
                pv = 2.0 * math.exp(-R * t_ex)
                shifted = dts.dividend_tree(
                    S0 - pv, K, R, SIG, T, STEPS, [], call=True, american=False
                )
                self.assertAlmostEqual(tree([(t_ex, 2.0)]), shifted, places=12)


class ExerciseLog(unittest.TestCase):
    """The log holds the time of each step at which some node exercises early."""

    def test_put_exercise_times_are_step_times(self) -> None:
        """An American put logs only step times before maturity, latest first."""
        log: list[float] = []
        dts.dividend_tree(S0, K, R, SIG, T, STEPS, [], call=False, exercise_log=log)
        dt = T / STEPS
        self.assertTrue(log)
        self.assertTrue(all(0 <= t < T for t in log))
        self.assertTrue(all(abs(t / dt - round(t / dt)) < 1e-9 for t in log))
        self.assertEqual(log, sorted(log, reverse=True))

    def test_no_dividend_call_never_exercises(self) -> None:
        """Without dividends an American call is never exercised early and equals the European."""
        log: list[float] = []
        am = dts.dividend_tree(S0, K, R, SIG, T, STEPS, [], call=True, exercise_log=log)
        self.assertEqual(log, [])
        self.assertAlmostEqual(am, tree([]), places=12)


if __name__ == "__main__":
    unittest.main()
