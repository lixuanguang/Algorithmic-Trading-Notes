"""Financial machine learning methods: supervised, unsupervised, leakage, text and evaluation.

Machine learning methods and the data-science workflow on synthetic data (2026-10-20).

Worked numbers of the entries in compendium/ml-alternative-data/machine-learning-methods.tex and
data-science-workflow.tex. Every dataset here is SYNTHETIC, generated with a fixed seed; nothing is
evidence about markets. The demonstrations show mechanics: overfitting against complexity, which
algorithm suits which data-generating process, what PCA and clustering recover, how fitted
transforms and look-ahead leak information, how text becomes features, and how a classifier is tuned
on a validation set and judged once on an untouched test set.

Splits are chronological (train, then validation, then test) unless stated; every transformation
(scaling, PCA, vocabulary, idf weights, feature selection) is fitted on the training rows only and
then applied to later rows.

Independent routes: ridge by the closed form against gradient descent; lasso by coordinate descent
against the KKT conditions; PCA by eigendecomposition against SVD; k-means objective decreasing
every iteration; hierarchical clusters from SciPy linkage against the planted groups; tf-idf by hand
against its definition; confusion-matrix metrics against their identities; ROC AUC by the trapezoid
rule against the Mann-Whitney statistic.

Count convention: one check is one executed ok() call (a call inside a loop counts once per
iteration). One generator, seeded 20261020, serves parts 1 to 6 in order; the forests and k-means
starts draw from their own generators, seeded per call.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.financial_ml_methods
(numpy, scipy). Exits 1 on failure.
"""

import math
import sys
from collections import Counter
from typing import Final, Literal

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.optimize import minimize
from scipy.stats import rankdata

from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]
# A fitted regression tree: a leaf's mean, or (feature, threshold, left subtree, right subtree).
type Tree = tuple[Literal["leaf"], float] | tuple[Literal["node"], np.intp, float, Tree, Tree]

SEED: Final = 20261020
STOP: Final = frozenset({"the", "a", "of", "and", "to", "in", "for", "is", "was", "on", "our"})


def mse(y: Floats, yhat: Floats) -> float:
    """Return the mean squared error of predictions yhat."""
    return float(np.mean((y - yhat) ** 2))


def split3(
    n: int, a: float = 0.6, b: float = 0.2
) -> tuple[slice[int, int, None], slice[int, int, None], slice[int, int, None]]:
    """Return chronological train, validation and test slices of n rows."""
    i1, i2 = int(n * a), int(n * (a + b))
    return slice(0, i1), slice(i1, i2), slice(i2, n)


def standardise(Xtr: Floats, X: Floats) -> Floats:
    """Return X standardised with the mean and standard deviation of the training rows Xtr."""
    mu, sd = Xtr.mean(0), Xtr.std(0)
    scaled: Floats = (X - mu) / sd
    return scaled


def ridge(X: Floats, y: Floats, lam: float) -> Floats:
    """Return the ridge coefficients (X'X + lam I)^-1 X'y."""
    p = X.shape[1]
    coef: Floats = np.asarray(np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y), dtype=np.float64)
    return coef


def lasso_cd(X: Floats, y: Floats, lam: float, iters: int = 500) -> Floats:
    """Coordinate descent for (1/2n)||y - Xb||^2 + lam ||b||_1 on standardised X."""
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
    return b


def tree_fit(
    X: Floats,
    y: Floats,
    depth: int,
    min_leaf: int = 5,
    feat_frac: float = 1.0,
    rng_: np.random.Generator | None = None,
) -> Tree:
    """Grow a regression tree of the given depth by the best squared-error split on decile cuts."""
    if depth == 0 or len(y) < 2 * min_leaf:
        return ("leaf", float(np.mean(y)))
    p_ = X.shape[1]
    feats: NDArray[np.intp] = np.arange(p_, dtype=np.intp)
    if feat_frac < 1.0:
        if rng_ is None:
            raise ValueError("a feature subsample needs a generator")
        feats = rng_.choice(p_, max(1, round(feat_frac * p_)), replace=False)
    best_: tuple[float, np.intp, float, NDArray[np.bool_]] | None = None
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
                best_ = (sse, j, s, left)
    if best_ is None:
        return ("leaf", float(np.mean(y)))
    _, j, s, left = best_
    return (
        "node",
        j,
        s,
        tree_fit(X[left], y[left], depth - 1, min_leaf, feat_frac, rng_),
        tree_fit(X[~left], y[~left], depth - 1, min_leaf, feat_frac, rng_),
    )


def tree_pred(t: Tree, X: Floats) -> Floats:
    """Return the predictions of tree t for the rows of X."""
    match t:
        case ("leaf", value):
            return np.full(len(X), value)
        case (_, j, s, lt, rt):
            out = np.empty(len(X))
            m = X[:, j] <= s
            out[m] = tree_pred(lt, X[m])
            out[~m] = tree_pred(rt, X[~m])
            return out


def forest(
    X: Floats, y: Floats, n_trees: int = 30, depth: int = 4, feat_frac: float = 0.6, seed: int = 1
) -> list[Tree]:
    """Return a random forest: bootstrap samples, each grown on a random feature subset."""
    g = np.random.default_rng(seed)
    trees: list[Tree] = []
    for _ in range(n_trees):
        b = g.integers(0, len(y), len(y))
        trees.append(tree_fit(X[b], y[b], depth, 5, feat_frac, g))
    return trees


def knn_pred(Xtr_: Floats, ytr_: NDArray[np.int64], Xq: Floats, k: int) -> NDArray[np.int64]:
    """Return the majority vote of the k nearest training rows for each query row."""
    d = ((Xq[:, None, :] - Xtr_[None, :, :]) ** 2).sum(-1)
    nn_idx = np.argsort(d, axis=1)[:, :k]
    votes: NDArray[np.int64] = (ytr_[nn_idx].mean(1) > 0.5).astype(np.int64)
    return votes


def svm_linear(X: Floats, y: NDArray[np.int64], C: float = 1.0) -> Floats:
    """Return the weights of a linear SVM with squared hinge loss, bias last."""
    ys_ = 2 * y - 1
    Xa = np.c_[X, np.ones(len(X))]

    def obj(w: Floats) -> float:
        margin = 1 - ys_ * (Xa @ w)
        return np.float64(0.5 * w[:-1] @ w[:-1] + C * np.sum(np.maximum(0, margin) ** 2))

    return minimize(obj, np.zeros(3), method="L-BFGS-B").x


def svm_pred(w: Floats, X: Floats) -> NDArray[np.int64]:
    """Return the 0/1 labels of a linear SVM with weights w, bias last."""
    labels: NDArray[np.int64] = (np.c_[X, np.ones(len(X))] @ w > 0).astype(np.int64)
    return labels


def kmeans(X: Floats, k: int, seed: int, iters: int = 50) -> tuple[NDArray[np.intp], list[float]]:
    """Return the labels and the within-cluster sum of squares per iteration of Lloyd's k-means."""
    g = np.random.default_rng(seed)
    cen = X[g.choice(len(X), k, replace=False)]
    hist: list[float] = []
    lab = np.zeros(len(X), dtype=np.intp)
    for _ in range(iters):
        d = ((X[:, None, :] - cen[None]) ** 2).sum(-1)
        lab = d.argmin(1)
        hist.append(float(d[np.arange(len(X)), lab].sum()))
        cen = np.array([X[lab == j].mean(0) if np.any(lab == j) else cen[j] for j in range(k)])
    return lab, hist


def tokens(s: str) -> list[str]:
    """Return the lower-cased words of s that are not stop words."""
    return [w for w in s.lower().split() if w not in STOP]


def chi2_score(col: NDArray[np.float64], y: NDArray[np.int64]) -> float:
    """Return the chi-square statistic of a word's presence against the class, 2x2 table."""
    pres = col > 0
    obs = np.array(
        [
            [np.sum(pres & (y == 1)), np.sum(pres & (y == 0))],
            [np.sum(~pres & (y == 1)), np.sum(~pres & (y == 0))],
        ]
    )
    exp_ = obs.sum(1, keepdims=True) * obs.sum(0, keepdims=True) / obs.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.nansum((obs - exp_) ** 2 / np.where(exp_ == 0, np.nan, exp_)))


def fit_logit(X: Floats, y: NDArray[np.int64], lam: float) -> Floats:
    """Return the L2-penalised logistic regression weights, bias last, by numerical minimisation."""
    Xa = np.c_[X, np.ones(len(X))]

    def loss(w: Floats) -> float:
        value = np.sum(np.log1p(np.exp(-(2 * y - 1) * (Xa @ w)))) + lam * w[:-1] @ w[:-1]
        return np.float64(value)

    return minimize(loss, np.zeros(Xa.shape[1])).x


def prob(w: Floats, X: Floats) -> Floats:
    """Return the logistic probabilities of the rows of X with weights w, bias last."""
    p: Floats = 1 / (1 + np.exp(-(np.c_[X, np.ones(len(X))] @ w)))
    return p


def logloss(y: NDArray[np.int64], p_: Floats) -> float:
    """Return the mean log loss of probabilities p_ against the 0/1 labels y."""
    p_ = np.clip(p_, 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p_) + (1 - y) * np.log(1 - p_)))


def check_overfitting(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 1: training error falls with complexity, validation error is U-shaped."""
    print(
        "== part 1: overfitting - training error falls with complexity, validation error is"
        " U-shaped (synthetic)"
    )
    n = 120
    x = np.sort(rng.uniform(-1, 1, n))
    y = np.sin(2.5 * x) + rng.normal(0, 0.3, n)
    idx = rng.permutation(n)  # cross-sectional toy data: a random split is legitimate here
    tr, va = idx[:80], idx[80:]
    train_err: dict[int, float] = {}
    val_err: dict[int, float] = {}
    for deg in range(1, 13):
        X = np.vander(x, deg + 1)
        beta, *_ = np.linalg.lstsq(X[tr], y[tr], rcond=None)
        train_err[deg] = mse(y[tr], X[tr] @ beta)
        val_err[deg] = mse(y[va], X[va] @ beta)
    best = min(val_err, key=lambda d: val_err[d])
    report.ok(
        "polynomial degree 1-12: training MSE never rises as degree grows; validation MSE is lowest"
        " at"
        f" a middle degree ({best}) and higher at degree 12 than at the best",
        all(train_err[d + 1] <= train_err[d] + 1e-12 for d in range(1, 12))
        and 2 <= best <= 8
        and val_err[12] > val_err[best],
        f"best degree {best}, val MSE {val_err[best]:.3f} vs {val_err[12]:.3f} at 12",
    )
    report.ok(
        "the best validation MSE is close to the noise variance 0.09 (irreducible error), so the"
        " remaining gap is bias plus variance",
        0.05 < val_err[best] < 0.15,
        f"{val_err[best]:.4f}",
    )


def check_supervised(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 2: match the method to the data-generating process."""
    print(
        "== part 2: supervised algorithms - match the method to the data-generating process"
        " (synthetic)"
    )
    # (a) sparse linear signal with many noise features: lasso
    nobs, p = 300, 40
    Xs = rng.normal(size=(nobs, p))
    beta_true = np.zeros(p)
    beta_true[:4] = [1.5, -1.0, 0.8, 0.5]
    ys = Xs @ beta_true + rng.normal(0, 1.0, nobs)
    trs, vas, tes = split3(nobs)
    Xtr = standardise(Xs[trs], Xs[trs])
    ytr = ys[trs] - ys[trs].mean()
    Xva = standardise(Xs[trs], Xs[vas])
    Xte = standardise(Xs[trs], Xs[tes])
    ols = np.linalg.lstsq(Xtr, ytr, rcond=None)[0]
    lams = [0.01, 0.03, 0.05, 0.1, 0.2, 0.3]
    val = {lam: mse(ys[vas] - ys[trs].mean(), Xva @ lasso_cd(Xtr, ytr, lam)) for lam in lams}
    lam_best = min(val, key=lambda k: val[k])
    b_l = lasso_cd(Xtr, ytr, lam_best)
    te_ols = mse(ys[tes] - ys[trs].mean(), Xte @ ols)
    te_lasso = mse(ys[tes] - ys[trs].mean(), Xte @ b_l)
    report.ok(
        "sparse linear truth (4 of 40 features matter): lasso with lambda chosen on validation"
        " beats"
        " OLS on the untouched test set and keeps the 4 true features while zeroing most noise"
        " features",
        te_lasso < te_ols and all(abs(b_l[:4]) > 0) and int(np.sum(np.abs(b_l[4:]) < 1e-12)) >= 25,
        f"test MSE lasso {te_lasso:.3f} vs OLS {te_ols:.3f}; lambda {lam_best}; zeros"
        f" {int(np.sum(np.abs(b_l[4:]) < 1e-12))}/36",
    )
    # KKT check for lasso: |X_j'r/n| <= lam with equality on active coefficients
    r = ytr - Xtr @ b_l
    grad = Xtr.T @ r / len(ytr)
    act = np.abs(b_l) > 1e-12
    report.ok(
        "lasso KKT conditions hold at the solution: correlations with the residual equal lambda"
        " (with"
        " the coefficient's sign) on active features and are at most lambda elsewhere",
        bool(
            np.allclose(grad[act], lam_best * np.sign(b_l[act]), atol=1e-6)
            and np.all(np.abs(grad[~act]) <= lam_best + 1e-6)
        ),
    )
    b_r = ridge(Xtr, ytr, 10.0)

    def ridge_loss(b: Floats) -> float:
        return np.float64(np.sum((ytr - Xtr @ b) ** 2) + 10.0 * b @ b)

    gd = minimize(ridge_loss, np.zeros(p), method="L-BFGS-B").x
    report.ok(
        "ridge shrinks without zeroing: the closed form (X'X + lambda I)^-1 X'y matches numerical"
        " minimisation, and no coefficient is exactly zero",
        bool(np.allclose(b_r, gd, atol=1e-4) and np.all(np.abs(b_r) > 1e-8)),
    )

    # (b) nonlinear interaction: tree ensembles
    nobs2 = 600
    X2 = rng.uniform(-1, 1, size=(nobs2, 5))
    y2 = 2.0 * ((X2[:, 0] > 0) & (X2[:, 1] > 0)) + rng.normal(0, 0.3, nobs2)
    tr2, va2, te2 = split3(nobs2)
    lin = np.linalg.lstsq(np.c_[np.ones(len(X2[tr2])), X2[tr2]], y2[tr2], rcond=None)[0]
    te_lin = mse(y2[te2], np.c_[np.ones(len(X2[te2])), X2[te2]] @ lin)
    depth_val = {
        d: mse(y2[va2], tree_pred(tree_fit(X2[tr2], y2[tr2], d), X2[va2])) for d in (1, 2, 3, 6, 10)
    }
    d_best = min(depth_val, key=lambda k: depth_val[k])
    te_tree = mse(y2[te2], tree_pred(tree_fit(X2[tr2], y2[tr2], d_best), X2[te2]))
    rf = forest(X2[tr2], y2[tr2])
    te_rf = mse(y2[te2], np.mean([tree_pred(t, X2[te2]) for t in rf], axis=0))
    report.ok(
        "interaction truth (y jumps by 2 only when x1 > 0 and x2 > 0): a tree with depth chosen on"
        " validation and a random forest both beat linear regression on the test set by a wide"
        " margin",
        te_tree < 0.6 * te_lin and te_rf < 0.6 * te_lin,
        f"test MSE linear {te_lin:.3f}, tree (depth {d_best}) {te_tree:.3f}, forest {te_rf:.3f}",
    )
    report.ok(
        "a depth-1 tree (one split) underfits the interaction: its validation error exceeds that of"
        " depth 2 or 3",
        depth_val[1] > min(depth_val[2], depth_val[3]),
        str({k: round(v, 3) for k, v in depth_val.items()}),
    )

    # (c) classification: KNN and a linear SVM against a circular and a linear boundary
    nobs3 = 600
    X3 = rng.normal(size=(nobs3, 2))
    y_circle = (np.sum(X3**2, axis=1) < 1.2).astype(int)
    y_line = (X3[:, 0] + 0.5 * X3[:, 1] + rng.normal(0, 0.3, nobs3) > 0).astype(int)
    tr3, va3, te3 = split3(nobs3)
    k_val = {
        k: np.mean(knn_pred(X3[tr3], y_circle[tr3], X3[va3], k) == y_circle[va3])
        for k in (1, 5, 15, 51)
    }
    k_best = max(k_val, key=lambda k: k_val[k])
    acc_knn_circle = np.mean(knn_pred(X3[tr3], y_circle[tr3], X3[te3], k_best) == y_circle[te3])
    acc_svm_circle = np.mean(svm_pred(svm_linear(X3[tr3], y_circle[tr3]), X3[te3]) == y_circle[te3])
    acc_svm_line = np.mean(svm_pred(svm_linear(X3[tr3], y_line[tr3]), X3[te3]) == y_line[te3])
    report.ok(
        "circular boundary: KNN (k chosen on validation) classifies the test set far better than a"
        " linear SVM, which cannot bend; with a linear boundary the linear SVM does well",
        acc_knn_circle > acc_svm_circle + 0.2 and acc_svm_line > 0.85,
        f"KNN {acc_knn_circle:.2f} (k={k_best}) vs linear SVM {acc_svm_circle:.2f} on the circle;"
        f" SVM {acc_svm_line:.2f} on the line",
    )


def check_unsupervised(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 3: PCA, k-means and hierarchical clustering on synthetic data."""
    print(
        "== part 3: unsupervised algorithms - PCA, k-means and hierarchical clustering (synthetic)"
    )
    T, N = 500, 10
    level = rng.normal(0, 1.0, T)
    slope = rng.normal(0, 0.5, T)
    load_level = np.ones(N)
    load_slope = np.linspace(-1, 1, N)
    R = np.outer(level, load_level) + np.outer(slope, load_slope) + rng.normal(0, 0.2, (T, N))
    trp = slice(0, 300)
    mu_tr = R[trp].mean(0)
    C = np.cov(R[trp] - mu_tr, rowvar=False)
    evals, evecs = np.linalg.eigh(C)
    evals, evecs = evals[::-1], evecs[:, ::-1]
    explained = evals / evals.sum()
    _, s_svd, _ = np.linalg.svd(R[trp] - mu_tr, full_matrices=False)
    report.ok(
        "PCA on 10 synthetic yields driven by a level and a slope factor: the first two components"
        " explain over 95% of training variance; eigenvalues of the covariance equal squared"
        " singular"
        " values / (n - 1)",
        explained[:2].sum() > 0.95 and np.allclose(evals[:5], s_svd[:5] ** 2 / (300 - 1)),
        f"{explained[:3].round(3)}",
    )
    report.ok(
        "the first component's loadings are nearly equal across maturities (level), the second's"
        " change sign (slope)",
        np.std(np.abs(evecs[:, 0])) < 0.02 and evecs[0, 1] * evecs[-1, 1] < 0,
    )
    centres = np.array([[0, 0], [3, 3], [0, 4]])
    G = np.vstack([c + rng.normal(0, 0.6, (60, 2)) for c in centres])
    labels_true = np.repeat([0, 1, 2], 60)
    runs = [kmeans(G, 3, s) for s in range(10)]
    lab_best, _ = min(runs, key=lambda r_: r_[1][-1])
    report.ok(
        "k-means (k = 3, 10 random starts): the within-cluster sum of squares never rises across"
        " iterations, and the best start recovers the three planted groups (each cluster is at"
        " least"
        " 95% one group)",
        all(all(h[i + 1] <= h[i] + 1e-9 for i in range(len(h) - 1)) for _, h in runs)
        and all(
            Counter(labels_true[lab_best == j]).most_common(1)[0][1] / max(1, np.sum(lab_best == j))
            >= 0.95
            for j in range(3)
        ),
    )
    wss = [min(kmeans(G, k, s)[1][-1] for s in range(5)) for k in range(1, 7)]
    report.ok(
        "the elbow: within-cluster sum of squares falls sharply up to k = 3 and slowly after",
        (wss[1] - wss[2]) > 3 * (wss[3] - wss[4]),
        f"{[round(w_) for w_ in wss]}",
    )
    Z = linkage(G, method="average")
    hc = fcluster(Z, 3, criterion="maxclust")
    purity = sum(Counter(labels_true[hc == c]).most_common(1)[0][1] for c in np.unique(hc)) / len(G)
    report.ok(
        "hierarchical clustering (average linkage, dendrogram cut at 3 clusters) recovers the"
        " groups"
        " with purity above 95% without choosing k in advance",
        purity > 0.95,
        f"purity {purity:.3f}",
    )


def check_leakage(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 4: look-ahead leakage, fitted transforms and winsorising outliers."""
    print("== part 4: data preparation, information timing and leakage (synthetic time series)")
    Tn = 1000
    z = np.cumsum(rng.normal(0, 1, Tn)) / 10  # a slow-moving, nonstationary feature
    ret = 0.0 * z + rng.normal(0, 1, Tn)  # the target has NO relation to z
    cut = 600
    # Look-ahead: using the next period's return (known only later) as a feature
    leak_feature = np.r_[ret[1:], 0.0]
    corr_true = np.corrcoef(z[:-1][cut:], ret[1:][cut:])[0, 1]
    corr_leak = np.corrcoef(leak_feature[:-1][cut:], ret[1:][cut:])[0, 1]
    report.ok(
        "look-ahead: a feature built from information released after the decision (next period's"
        " return) shows perfect test correlation with the target, while the honest feature shows"
        " none",
        abs(corr_leak) > 0.99 and abs(corr_true) < 0.15,
        f"honest {corr_true:.3f}, leaked {corr_leak:.3f}",
    )
    mu_full, sd_full = z.mean(), z.std()
    mu_tr4, sd_tr4 = z[:cut].mean(), z[:cut].std()
    report.ok(
        "fitted transforms: standardising with full-sample mean and s.d. uses test-period"
        " information;"
        " the training-only statistics differ materially for a trending feature, so the test inputs"
        " are shifted",
        abs(mu_full - mu_tr4) > 0.1 * sd_tr4 or abs(sd_full / sd_tr4 - 1) > 0.1,
        f"mean full {mu_full:.3f} vs train {mu_tr4:.3f}; s.d. {sd_full:.3f} vs {sd_tr4:.3f}",
    )
    raw = np.r_[rng.normal(0, 1, 995), [25, -30, 40, 18, -22]]
    lo, hi = np.quantile(raw[:800], [0.01, 0.99])
    wins = np.clip(raw, lo, hi)
    report.ok(
        "outliers: winsorising at the 1st and 99th training percentiles caps the five planted"
        " errors"
        " without dropping rows; the s.d. falls from above 2 to about 1",
        raw.std() > 2 and abs(wins.std() - 1) < 0.15,
        f"{raw.std():.2f} -> {wins.std():.2f}",
    )


def check_text(report: CheckReport) -> None:
    """Part 5: tokens, a document-term matrix, tf-idf and chi-square selection on a toy corpus."""
    print(
        "== part 5: text features - tokens, a document-term matrix, tf-idf, chi-square selection"
        " (synthetic corpus)"
    )
    docs = [
        ("revenue growth strong and margins improved for the quarter", 1),
        ("strong demand drove record revenue and growth", 1),
        ("margins improved on lower costs and strong pricing", 1),
        ("guidance raised on strong demand", 1),
        ("impairment charge and weak demand in the quarter", 0),
        ("revenue declined on weak pricing and higher costs", 0),
        ("guidance lowered after impairment and litigation", 0),
        ("weak margins and litigation costs hurt the quarter", 0),
        ("record growth in demand and strong margins", 1),
        ("litigation and impairment drove a loss", 0),
    ]
    train_docs, test_docs = docs[:8], docs[8:]
    vocab = sorted(
        {w for d, _ in train_docs for w in tokens(d)}
    )  # vocabulary from training documents only
    DTM = np.array([[tokens(d).count(w) for w in vocab] for d, _ in train_docs], dtype=float)
    ytxt = np.array([lab for _, lab in train_docs])
    df = (DTM > 0).sum(0)
    idf = np.log(len(train_docs) / df)
    tfidf = DTM * idf
    j_strong = vocab.index("strong")
    report.ok(
        "the vocabulary is built on the 8 training documents only (stop words removed); 'strong'"
        " appears in 4 of them, so idf = ln(8/4) = 0.693 and its tf-idf in document 1 is 0.693",
        df[j_strong] == 4
        and math.isclose(idf[j_strong], math.log(2))
        and math.isclose(tfidf[0, j_strong], math.log(2)),
    )
    scores = {w: chi2_score(DTM[:, i], ytxt) for i, w in enumerate(vocab)}
    top = sorted(scores, key=lambda w: scores[w], reverse=True)[:4]
    report.ok(
        "chi-square feature selection on the training documents ranks class-specific words"
        " ('strong',"
        " 'weak', 'impairment', 'litigation') above neutral ones ('quarter', 'revenue')",
        {"strong", "weak"} <= set(top)
        and scores["quarter"] < scores["strong"]
        and scores["revenue"] < scores["strong"],
        f"top: {top}",
    )
    sel = [vocab.index(w) for w in top]
    Xtxt = (DTM[:, sel] > 0).astype(float)

    def text_loss(w: Floats) -> float:
        return np.float64(
            np.sum(np.log1p(np.exp(-(2 * ytxt - 1) * (np.c_[Xtxt, np.ones(8)] @ w)))) + 0.1 * w @ w
        )

    wlog = minimize(text_loss, np.zeros(len(sel) + 1)).x
    Xtest = np.array([[1.0 if w in tokens(d) else 0.0 for w in top] for d, _ in test_docs])
    pred_test = (np.c_[Xtest, np.ones(len(Xtest))] @ wlog > 0).astype(int)
    report.ok(
        "a regularised logistic classifier on the selected words labels both held-out documents"
        " correctly (a toy: two test documents prove nothing about real filings)",
        list(pred_test) == [lab for _, lab in test_docs],
    )


def check_classifier(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 6: validation tuning of a logistic classifier, test metrics and the ROC curve."""
    print(
        "== part 6: training and evaluating a classifier - validation tuning, test metrics, ROC"
        " (synthetic)"
    )
    nn6 = 2000
    X6 = rng.normal(size=(nn6, 3))
    logit = 1.2 * X6[:, 0] - 0.8 * X6[:, 1] - 1.5
    p_true = 1 / (1 + np.exp(-logit))
    y6 = (rng.uniform(size=nn6) < p_true).astype(int)
    tr6, va6, te6 = split3(nn6)
    val_ll = {
        lam: logloss(y6[va6], prob(fit_logit(X6[tr6], y6[tr6], lam), X6[va6]))
        for lam in (0.0, 1.0, 10.0, 100.0)
    }
    lam6 = min(val_ll, key=lambda k: val_ll[k])
    w6 = fit_logit(X6[tr6], y6[tr6], lam6)
    p_te = prob(w6, X6[te6])
    pred = (p_te > 0.5).astype(int)
    yt = y6[te6]
    tp, fp = int(np.sum((pred == 1) & (yt == 1))), int(np.sum((pred == 1) & (yt == 0)))
    fn, tn = int(np.sum((pred == 0) & (yt == 1))), int(np.sum((pred == 0) & (yt == 0)))
    precision, recall = tp / (tp + fp), tp / (tp + fn)
    accuracy = (tp + tn) / len(yt)
    f1 = 2 * precision * recall / (precision + recall)
    report.ok(
        "the penalty is chosen on the validation set only; on the untouched test set the confusion"
        " matrix gives precision, recall, accuracy and F1 consistent with their definitions (F1 ="
        " harmonic mean)",
        tp + fp + fn + tn == len(yt) and math.isclose(1 / f1, 0.5 * (1 / precision + 1 / recall)),
        f"lambda {lam6}; TP {tp} FP {fp} FN {fn} TN {tn}; P {precision:.2f} R {recall:.2f} acc"
        f" {accuracy:.2f} F1 {f1:.2f}",
    )
    base_rate = yt.mean()
    report.ok(
        "with a minority positive class (about a quarter of cases) accuracy flatters: always"
        " predicting"
        " 'negative' would score 1 - base rate, so recall and precision must be reported",
        base_rate < 0.35 and (1 - base_rate) > 0.65,
        f"base rate {base_rate:.2f}",
    )
    order = np.argsort(-p_te)
    tpr = np.r_[0, np.cumsum(yt[order] == 1) / yt.sum()]
    fpr = np.r_[0, np.cumsum(yt[order] == 0) / (1 - yt).sum()]
    auc_trap = float(np.sum((fpr[1:] - fpr[:-1]) * (tpr[1:] + tpr[:-1]) / 2))
    ranks = rankdata(p_te)
    auc_mw = (ranks[yt == 1].sum() - yt.sum() * (yt.sum() + 1) / 2) / (yt.sum() * (1 - yt).sum())
    report.ok(
        "ROC AUC by the trapezoid rule equals the Mann-Whitney probability that a random positive"
        " scores above a random negative",
        abs(auc_trap - auc_mw) < 1e-9 and 0.75 < auc_mw < 0.95,
        f"AUC {auc_mw:.3f}",
    )
    thr = {
        t_: (
            np.sum((p_te > t_) & (yt == 1)) / yt.sum(),
            np.sum((p_te > t_) & (yt == 0)) / (1 - yt).sum(),
        )
        for t_ in (0.2, 0.5)
    }
    report.ok(
        "lowering the threshold from 0.5 to 0.2 raises recall and the false-positive rate together:"
        " the threshold is a business choice set on validation data, not a property of the model",
        thr[0.2][0] > thr[0.5][0] and thr[0.2][1] > thr[0.5][1],
    )


def main() -> int:
    """Print the versions, then run the six parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    check_overfitting(report, rng)
    check_supervised(report, rng)
    check_unsupervised(report, rng)
    check_leakage(report, rng)
    check_text(report)
    check_classifier(report, rng)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
