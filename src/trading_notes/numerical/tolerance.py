"""Absolute-tolerance comparison shared by the numerical checks."""


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol.

    The tolerance is absolute, not relative; a NaN or infinite difference is never close.
    """
    return abs(a - b) <= tol
