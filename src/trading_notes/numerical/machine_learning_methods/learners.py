"""Small reference learners on NumPy arrays: penalised regressions, trees, SVMs, logit, k-means."""

from typing import Self

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Labels = NDArray[np.int64]


class RidgeRegression(Record):
    """Ridge regression through the origin.

    Attributes:
        coefficients: (X'X + lam I)^-1 X'y.
    """

    coefficients: Floats

    @classmethod
    def fit(cls, X: Floats, y: Floats, lam: float) -> Self:
        """Return the fit of y on the columns of X with penalty lam ||b||^2."""
        p = X.shape[1]
        return cls(
            coefficients=np.asarray(
                np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y), dtype=np.float64
            )
        )

    def predict(self, X: Floats) -> Floats:
        """Return the fitted values X b for the rows of X."""
        fitted: Floats = X @ self.coefficients
        return fitted


class LassoRegression(Record):
    """The lasso through the origin, by cyclic coordinate descent.

    Attributes:
        coefficients: The minimiser of (1/2n)||y - Xb||^2 + lam ||b||_1.
    """

    coefficients: Floats

    @classmethod
    def fit(cls, X: Floats, y: Floats, lam: float, iters: int = 500) -> Self:
        """Return the fit after iters sweeps from zero; X is expected standardised."""
        nn, p = X.shape
        b = np.zeros(p)
        r = y - X @ b
        for _ in range(iters):
            for j in range(p):
                r += X[:, j] * b[j]
                rho = X[:, j] @ r / nn
                zj = X[:, j] @ X[:, j] / nn
                b[j] = np.sign(rho) * max(abs(rho) - lam, 0) / zj
                r -= X[:, j] * b[j]
        return cls(coefficients=b)

    def predict(self, X: Floats) -> Floats:
        """Return the fitted values X b for the rows of X."""
        fitted: Floats = X @ self.coefficients
        return fitted


class NearestNeighbours(Record):
    """A k-nearest-neighbour classifier of 0/1 labels by squared Euclidean distance.

    Attributes:
        features: The training rows.
        labels: Their 0/1 labels.
        k: How many neighbours vote.
    """

    features: Floats
    labels: Labels
    k: int

    def predict(self, X: Floats) -> Labels:
        """Return the majority vote of the k nearest training rows for each row of X."""
        d = ((X[:, None, :] - self.features[None, :, :]) ** 2).sum(-1)
        nn_idx = np.argsort(d, axis=1)[:, : self.k]
        votes: Labels = (self.labels[nn_idx].mean(1) > 0.5).astype(np.int64)
        return votes


class Leaf(Record):
    """A terminal node predicting its training rows' mean.

    Attributes:
        value: The mean.
    """

    value: float

    def predict(self, X: Floats) -> Floats:
        """Return the value for every row of X."""
        return np.full(len(X), self.value)


class Split(Record):
    """An internal node sending rows with x_feature <= threshold left.

    Attributes:
        feature: The column split on.
        threshold: The cut.
        left: The subtree of rows at or below the cut.
        right: The subtree of rows above it.
    """

    feature: int
    threshold: float
    left: Leaf | Split
    right: Leaf | Split

    def predict(self, X: Floats) -> Floats:
        """Return each row's prediction from the subtree its feature value sends it to."""
        out = np.empty(len(X))
        m = X[:, self.feature] <= self.threshold
        out[m] = self.left.predict(X[m])
        out[~m] = self.right.predict(X[~m])
        return out


class RegressionTree(Record):
    """A regression tree grown by the best squared-error split on decile cuts.

    Attributes:
        root: The root node.
    """

    root: Leaf | Split

    @classmethod
    def fit(
        cls,
        X: Floats,
        y: Floats,
        depth: int,
        min_leaf: int = 5,
        feat_frac: float = 1.0,
        rng: np.random.Generator | None = None,
    ) -> Self:
        """Return the tree of the given depth; feat_frac < 1 draws features at each node.

        Raises:
            ValueError: If a feature subsample is asked for without a generator.
        """
        return cls(root=_grow(X, y, depth, min_leaf, feat_frac, rng))

    def predict(self, X: Floats) -> Floats:
        """Return the predictions for the rows of X."""
        return self.root.predict(X)


def _grow(
    X: Floats,
    y: Floats,
    depth: int,
    min_leaf: int,
    feat_frac: float,
    rng: np.random.Generator | None,
) -> Leaf | Split:
    """Return the node splitting y best on decile cuts of the (sampled) features, recursively."""
    if depth == 0 or len(y) < 2 * min_leaf:
        return Leaf(value=float(np.mean(y)))
    p_ = X.shape[1]
    feats: NDArray[np.intp] = np.arange(p_, dtype=np.intp)
    if feat_frac < 1.0:
        if rng is None:
            raise ValueError("a feature subsample needs a generator")
        feats = rng.choice(p_, max(1, round(feat_frac * p_)), replace=False)
    best_: tuple[float, int, float, NDArray[np.bool_]] | None = None
    for j in feats:
        qs = np.quantile(X[:, j], np.linspace(0.1, 0.9, 9))
        for s in qs:
            left = X[:, j] <= s
            if left.sum() < min_leaf or (~left).sum() < min_leaf:
                continue
            sse = ((y[left] - y[left].mean()) ** 2).sum() + (
                (y[~left] - y[~left].mean()) ** 2
            ).sum()
            if best_ is None or sse < best_[0]:
                best_ = (float(sse), int(j), float(s), left)
    if best_ is None:
        return Leaf(value=float(np.mean(y)))
    _, j, s, left = best_
    return Split(
        feature=j,
        threshold=s,
        left=_grow(X[left], y[left], depth - 1, min_leaf, feat_frac, rng),
        right=_grow(X[~left], y[~left], depth - 1, min_leaf, feat_frac, rng),
    )


class RandomForest(Record):
    """Trees grown on bootstrap samples, each split on a random subset of features.

    Attributes:
        trees: The trees.
    """

    trees: tuple[RegressionTree, ...]

    @classmethod
    def fit(
        cls,
        X: Floats,
        y: Floats,
        n_trees: int = 30,
        depth: int = 4,
        feat_frac: float = 0.6,
        seed: int = 1,
    ) -> Self:
        """Return the forest, from a generator of its own seeded with seed."""
        g = np.random.default_rng(seed)
        trees: list[RegressionTree] = []
        for _ in range(n_trees):
            b = g.integers(0, len(y), len(y))
            trees.append(RegressionTree.fit(X[b], y[b], depth, 5, feat_frac, g))
        return cls(trees=tuple(trees))

    def predict(self, X: Floats) -> Floats:
        """Return the mean of the trees' predictions."""
        pred: Floats = np.mean([t.predict(X) for t in self.trees], axis=0)
        return pred


class LinearSvm(Record):
    """A linear SVM with squared hinge loss on two features.

    Attributes:
        weights: The two feature weights, then the bias.
    """

    weights: Floats

    @classmethod
    def fit(cls, X: Floats, y: Labels, C: float = 1.0) -> Self:
        """Return the SVM for 0/1 labels, by L-BFGS-B from zero weights."""
        ys_ = 2 * y - 1
        Xa = np.c_[X, np.ones(len(X))]

        def obj(w: Floats) -> float:
            margin = 1 - ys_ * (Xa @ w)
            return float(0.5 * w[:-1] @ w[:-1] + C * np.sum(np.maximum(0, margin) ** 2))

        return cls(weights=minimize(obj, np.zeros(3), method="L-BFGS-B").x)

    def predict(self, X: Floats) -> Labels:
        """Return the 0/1 labels of the rows of X."""
        labels: Labels = (np.c_[X, np.ones(len(X))] @ self.weights > 0).astype(np.int64)
        return labels


class LogisticModel(Record):
    """L2-penalised logistic regression.

    Attributes:
        weights: The feature weights, then the unpenalised bias.
    """

    weights: Floats

    @classmethod
    def fit(cls, X: Floats, y: Labels, lam: float) -> Self:
        """Return the model for 0/1 labels, by numerical minimisation from zero weights."""
        Xa = np.c_[X, np.ones(len(X))]

        def loss(w: Floats) -> float:
            return float(np.sum(np.log1p(np.exp(-(2 * y - 1) * (Xa @ w)))) + lam * w[:-1] @ w[:-1])

        return cls(weights=minimize(loss, np.zeros(Xa.shape[1])).x)

    def probabilities(self, X: Floats) -> Floats:
        """Return the probabilities of label 1 for the rows of X."""
        p: Floats = 1 / (1 + np.exp(-(np.c_[X, np.ones(len(X))] @ self.weights)))
        return p


class KMeansFit(Record):
    """Lloyd's k-means from k distinct rows drawn as starting centres.

    Attributes:
        labels: Each row's cluster after the last iteration.
        history: The within-cluster sum of squares at each iteration.
    """

    labels: NDArray[np.intp]
    history: list[float]

    @classmethod
    def fit(cls, X: Floats, k: int, seed: int, iters: int = 50) -> Self:
        """Return the fit, its starts drawn from a generator of its own seeded with seed."""
        g = np.random.default_rng(seed)
        cen = X[g.choice(len(X), k, replace=False)]
        hist: list[float] = []
        lab = np.zeros(len(X), dtype=np.intp)
        for _ in range(iters):
            d = ((X[:, None, :] - cen[None]) ** 2).sum(-1)
            lab = d.argmin(1)
            hist.append(float(d[np.arange(len(X)), lab].sum()))
            cen = np.array([X[lab == j].mean(0) if np.any(lab == j) else cen[j] for j in range(k)])
        return cls(labels=lab, history=hist)
