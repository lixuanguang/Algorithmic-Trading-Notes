"""Tests of the dividend tree's date conventions and its exercise log."""

import math
import unittest

from trading_notes.numerical.option_valuation.dividend_tree import KnownDividendTree

S0, K, R, SIG, T, STEPS = 50.0, 50.0, 0.05, 0.25, 0.5, 200


def tree(divs: list[tuple[float, float]], *, call: bool = True, american: bool = False) -> float:
    """Return the tree value at the module's test inputs."""
    return KnownDividendTree(
        spot=S0, strike=K, rate=R, vol=SIG, maturity=T, steps=STEPS, dividends=divs
    ).value(call=call, american=american)


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
                shifted = KnownDividendTree(
                    spot=S0 - pv, strike=K, rate=R, vol=SIG, maturity=T, steps=STEPS, dividends=[]
                ).value(call=True, american=False)
                self.assertAlmostEqual(tree([(t_ex, 2.0)]), shifted, places=12)


class ExerciseLog(unittest.TestCase):
    """The log holds the time of each step at which some node exercises early."""

    def test_put_exercise_times_are_step_times(self) -> None:
        """An American put logs only step times before maturity, latest first."""
        log: list[float] = []
        KnownDividendTree(
            spot=S0, strike=K, rate=R, vol=SIG, maturity=T, steps=STEPS, dividends=[]
        ).value(call=False, exercise_log=log)
        dt = T / STEPS
        self.assertTrue(log)
        self.assertTrue(all(0 <= t < T for t in log))
        self.assertTrue(all(abs(t / dt - round(t / dt)) < 1e-9 for t in log))
        self.assertEqual(log, sorted(log, reverse=True))

    def test_no_dividend_call_never_exercises(self) -> None:
        """Without dividends an American call is never exercised early and equals the European."""
        log: list[float] = []
        am = KnownDividendTree(
            spot=S0, strike=K, rate=R, vol=SIG, maturity=T, steps=STEPS, dividends=[]
        ).value(call=True, exercise_log=log)
        self.assertEqual(log, [])
        self.assertAlmostEqual(am, tree([]), places=12)


if __name__ == "__main__":
    unittest.main()
