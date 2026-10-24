"""Ledoit and Wolf's oracle linear shrinkage of a sample covariance toward a scaled identity."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def frob(A: Floats) -> float:
    """Return the scaled squared Frobenius norm Tr(A'A)/N of an N x N matrix."""
    return float(np.trace(A.T @ A) / A.shape[0])


def gmv_var(C: Floats, Sigma: Floats) -> float:
    """Return the true variance w' Sigma w of the GMV portfolio built from the estimate C.

    Args:
        C: Covariance estimate, N x N.
        Sigma: True covariance, N x N.
    """
    w = np.linalg.solve(C, np.ones(C.shape[0]))
    w /= w.sum()
    return float(w @ Sigma @ w)


class OracleShrinkage(Record):
    """The simulation's estimates, as averages over the samples where they are expectations.

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


class ShrinkageExperiment(Record):
    """Mean-zero normal samples from a one-factor population with known covariance.

    Attributes:
        assets: N, the number of assets.
        observations: T, the observations in each sample.
        samples: R, the number of simulated samples.
        seed: The seed of the experiment's own generator.
    """

    assets: int
    observations: int
    samples: int
    seed: int

    def run(self) -> OracleShrinkage:
        """Run the experiment with a generator of its own.

        The generator draws, in order, the factor loadings, the idiosyncratic variances and
        then the R observation matrices, each T x N.
        """
        n = self.assets
        rng = np.random.default_rng(self.seed)
        beta = rng.normal(1.0, 0.3, n)
        Sigma = 0.04 * np.outer(beta, beta) + np.diag(rng.uniform(0.01, 0.09, n))
        L = np.linalg.cholesky(Sigma)
        mu = np.trace(Sigma) / n
        identity = np.eye(n)
        alpha2 = frob(Sigma - mu * identity)
        Ss = []
        for _ in range(self.samples):
            X = rng.standard_normal((self.observations, n)) @ L.T
            Ss.append(X.T @ X / self.observations)  # mean-zero data, as in the paper's Section 2
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
            var_oracle=float(
                np.mean([gmv_var(g * mu * identity + (1 - g) * S, Sigma) for S in Ss])
            ),
            var_true=gmv_var(Sigma, Sigma),
        )
