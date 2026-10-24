"""Own simulation behind meth:portfolio-covariance-estimation.

Source verification (2026-10-17). Ledoit and Wolf's review (UZH WP 323, version of February 2020,
eqs. (2.4)-(2.7), pp. 5-6) gives the oracle linear shrinkage Sigma* = gamma* mu I +
(1 - gamma*) S, gamma* = beta^2 / delta^2, mu = <Sigma, I>, with the scaled Frobenius norm
||A||^2 = Tr(A'A)/N, beta^2 = E||S - Sigma||^2, delta^2 = E||S - mu I||^2 = alpha^2 + beta^2.
Checked here, with the population known (so the oracle is computable): N = 100 assets, T = 120
i.i.d. normal observations, a true covariance with a one-factor structure. (1) the identity
alpha^2 + beta^2 = delta^2 holds by simulation; (2) the oracle has lower Frobenius loss than S;
(3) the global minimum-variance portfolio built from Sigma* has a lower true variance than the
one built from S. Synthetic data only; the feasible estimator of the paper is not reproduced.
Only failed conditions are reported, each as a BAD line.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.covariance_shrinkage
(numpy). Exits non-zero on failure.
"""

import sys
from dataclasses import dataclass
from typing import Final

import numpy as np
from numpy.typing import NDArray

N: Final = 100  # assets
T: Final = 120  # observations per sample
R: Final = 300  # simulated samples
SEED: Final = 2020


@dataclass(frozen=True)
class OracleShrinkage:
    """The simulation's estimates, as averages over the R samples where they are expectations.

    Attributes:
        alpha2: ||Sigma - mu I||^2, from the population.
        beta2: E||S - Sigma||^2, which is also the sample covariance's Frobenius loss.
        delta2: E||S - mu I||^2.
        gamma: The oracle intensity beta^2 / delta^2.
        loss_oracle: E||Sigma* - Sigma||^2.
        var_sample: Mean true variance of the GMV portfolio built from S.
        var_oracle: Mean true variance of the GMV portfolio built from Sigma*.
        var_true: True variance of the GMV portfolio built from Sigma.
    """

    alpha2: float
    beta2: float
    delta2: float
    gamma: float
    loss_oracle: float
    var_sample: float
    var_oracle: float
    var_true: float


def frob(A: NDArray[np.float64]) -> float:
    """Return the scaled squared Frobenius norm Tr(A'A)/N of an N x N matrix."""
    return float(np.trace(A.T @ A) / N)


def gmv_var(C: NDArray[np.float64], Sigma: NDArray[np.float64]) -> float:
    """Return the true variance w' Sigma w of the GMV portfolio built from the estimate C.

    Args:
        C: Covariance estimate, N x N.
        Sigma: True covariance, N x N.
    """
    w = np.linalg.solve(C, np.ones(N))
    w /= w.sum()
    return float(w @ Sigma @ w)


def simulate() -> OracleShrinkage:
    """Run the simulation with a generator of its own, seeded with SEED.

    The generator draws, in order, the factor loadings, the idiosyncratic variances and then
    the R observation matrices, each T x N.
    """
    rng = np.random.default_rng(SEED)
    beta = rng.normal(1.0, 0.3, N)
    Sigma = 0.04 * np.outer(beta, beta) + np.diag(rng.uniform(0.01, 0.09, N))
    L = np.linalg.cholesky(Sigma)
    mu = np.trace(Sigma) / N
    identity = np.eye(N)
    alpha2 = frob(Sigma - mu * identity)
    Ss = []
    for _ in range(R):
        X = rng.standard_normal((T, N)) @ L.T
        Ss.append(X.T @ X / T)  # mean-zero data, as in the paper's Section 2
    beta2 = float(np.mean([frob(S - Sigma) for S in Ss]))
    delta2 = float(np.mean([frob(S - mu * identity) for S in Ss]))
    g = beta2 / delta2
    return OracleShrinkage(
        alpha2=alpha2,
        beta2=beta2,
        delta2=delta2,
        gamma=g,
        loss_oracle=float(np.mean([frob(g * mu * identity + (1 - g) * S - Sigma) for S in Ss])),
        var_sample=float(np.mean([gmv_var(S, Sigma) for S in Ss])),
        var_oracle=float(np.mean([gmv_var(g * mu * identity + (1 - g) * S, Sigma) for S in Ss])),
        var_true=gmv_var(Sigma, Sigma),
    )


def failed_conditions(run: OracleShrinkage) -> list[str]:
    """Return the names of the three conditions that fail, in order.

    The identity is accepted within 2% of delta^2; the two improvements must be strict.
    """
    fails = []
    if abs(run.alpha2 + run.beta2 - run.delta2) > 0.02 * run.delta2:
        fails.append("identity")
    if not run.loss_oracle < run.beta2:
        fails.append("Frobenius")
    if not run.var_oracle < run.var_sample:
        fails.append("GMV variance")
    return fails


def main() -> int:
    """Run the simulation, print its estimates and any failures; return 0, or 1 on failure."""
    run = simulate()
    print(
        f"alpha^2 + beta^2 = {run.alpha2 + run.beta2:.6f}, delta^2 = {run.delta2:.6f}; "
        f"oracle intensity gamma* = {run.gamma:.3f}"
    )
    print(f"Frobenius loss: sample {run.beta2:.6f}, oracle shrinkage {run.loss_oracle:.6f}")
    print(
        f"true variance of GMV portfolio: from S {run.var_sample:.6f}, "
        f"from Sigma* {run.var_oracle:.6f}, true optimum {run.var_true:.6f}"
    )
    fails = failed_conditions(run)
    for f in fails:
        print("BAD", f)
    if fails:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
