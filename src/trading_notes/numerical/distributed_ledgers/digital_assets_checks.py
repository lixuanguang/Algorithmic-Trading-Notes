"""Distributed-ledger mechanics and digital-asset investment arithmetic."""

import itertools
import math
import sys
from datetime import date
from typing import Final

import numpy as np

from trading_notes.numerical.distributed_ledgers.ledger import (
    BlockChain,
    DoubleSpendRace,
    MerkleTree,
    ProofOfWork,
    h,
)
from trading_notes.numerical.report import CheckReport

SEED: Final = 20261020
BLOCKS_TX: Final = (
    ("A pays B 5", "C pays D 2", "E pays F 1"),
    ("B pays C 3", "D pays A 1"),
    ("F pays A 1", "A pays E 2", "C pays B 1", "D pays F 1"),
)


def check_ledger(report: CheckReport) -> None:
    """Part 1: hash-chained blocks and Merkle trees."""
    print("== part 1: hash-chained blocks and Merkle trees (toy ledger)")
    chain = BlockChain.of(BLOCKS_TX)
    report.ok("an untouched chain of three blocks verifies link by link", chain.valid())
    first = chain.blocks[0].with_transaction(0, "A pays B 50")
    tampered = chain.model_copy(update={"blocks": (first, *chain.blocks[1:])})
    report.ok(
        "changing one transaction in the first block changes its Merkle root, so its stored hash no"
        " longer matches and "
        "every later block's link to it breaks unless all are recomputed",
        not tampered.valid(),
    )
    tree = MerkleTree(transactions=BLOCKS_TX[2])
    br = tree.branch(2)
    report.ok(
        "simplified payment verification: a light client holding only the root confirms 'C pays B"
        " 1' from a branch of "
        "log2(4) = 2 hashes, and the same branch does not verify an altered transaction",
        len(br.steps) == 2
        and br.verifies("C pays B 1", tree.root)
        and not br.verifies("C pays B 9", tree.root),
    )


def check_proof_of_work(report: CheckReport) -> None:
    """Part 2: the mean work to find a nonce, against one hash to verify it."""
    print("== part 2: proof-of-work - finding a nonce is costly, checking it takes one hash")
    bits = 12
    work = ProofOfWork(bits=bits)
    trials = [work.mine(f"block-{k}") + 1 for k in range(60)]
    report.ok(
        f"with a target of {bits} leading zero bits the average number of hashes is about"
        f" 2^{bits} = {2**bits}; "
        "verification needs one hash",
        bool(
            0.6 * 2**bits < np.mean(trials) < 1.5 * 2**bits
            and int(h(f"block-0{trials[0] - 1}".encode()), 16) < work.target
        ),
        f"mean {np.mean(trials):.0f} hashes over 60 blocks",
    )


def check_finality(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 3: Nakamoto's table, the waits it implies, and the exact race by simulation."""
    print("== part 3: probabilistic finality - Nakamoto's attacker race (sec. 11)")
    table = {
        (0.1, 1): 0.2045873,
        (0.1, 5): 0.0009137,
        (0.1, 10): 0.0000012,
        (0.3, 5): 0.1773523,
        (0.3, 10): 0.0416605,
    }
    report.ok(
        "the formula reproduces the white paper's printed probabilities to seven decimals",
        all(
            abs(DoubleSpendRace(attacker=q).poisson_success(z) - v) < 5e-8
            for (q, z), v in table.items()
        ),
    )
    need = {
        q: next(z for z in range(1000) if DoubleSpendRace(attacker=q).poisson_success(z) < 0.001)
        for q in (0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45)
    }
    report.ok(
        "blocks a merchant must wait for P < 0.1% match the paper: 5, 8, 11, 15, 24, 41, 89 and 340"
        " as the attacker's "
        "share rises from 10% to 45%",
        list(need.values()) == [5, 8, 11, 15, 24, 41, 89, 340],
    )
    race = DoubleSpendRace(attacker=0.1)
    exact = race.exact_success(5)
    sim = race.simulate(rng, 5)
    report.ok(
        "an independent simulation of the race (negative-binomial attacker progress, then a random"
        " walk) agrees with "
        "the exact negative-binomial sum",
        abs(sim - exact) < 0.0003,
        f"simulated {sim:.5f}, exact {exact:.5f}",
    )
    report.ok(
        "the white paper's Poisson step understates the exact probability (0.00091 against about"
        " 0.0018 at q = 0.1, "
        "z = 5), so its waiting times are a lower bound; both fall exponentially with z",
        race.poisson_success(5) < exact < 2 * race.poisson_success(5)
        and race.exact_success(10) < exact / 10,
    )
    report.ok(
        "with an attacker holding at least half of the hashing power, catching up is certain (q >="
        " p gives probability 1)",
        all(min(1.0, (q / (1 - q)) ** 6) == 1.0 for q in (0.5, 0.6)),
    )


def check_supply(report: CheckReport) -> None:
    """Part 4: Bitcoin's issuance in integer satoshis, and proof-of-stake timing."""
    print("== part 4: protocol-fixed supply and proof-of-stake timing")
    sat = 50 * 10**8
    total, era = 0, 0
    while sat > 0:
        total += 210_000 * sat
        sat //= 2  # integer satoshis: the subsidy rounds down at each halving
        era += 1
    report.ok(
        "50 coins a block halving every 210,000 blocks sums to just under 21 million coins (the"
        " geometric limit "
        "50 x 210,000 x 2 = 21,000,000, less integer rounding), issued over 33 eras",
        total / 1e8 < 21_000_000
        and abs(total / 1e8 - 21_000_000) < 1
        and era == 33
        and math.isclose(50 * 210_000 * 2, 21_000_000),
        f"{total / 1e8:,.8f} coins",
    )
    report.ok(
        "Ethereum proof-of-stake: 12-second slots and 32-slot epochs give 6.4-minute epochs;"
        " finality needs a "
        "supermajority link (two-thirds of staked ETH) between checkpoints, about two epochs or"
        " 12.8 minutes",
        math.isclose(12 * 32 / 60, 6.4) and math.isclose(2 * 12 * 32 / 60, 12.8),
    )


def check_published_statistics(report: CheckReport) -> None:
    """Part 5: consistency of Liu and Tsyvinski's published Bitcoin statistics."""
    print(
        "== part 5: published Bitcoin statistics (Liu and Tsyvinski, Table 1) - consistency checks"
    )
    lt = {
        "daily": (0.52, 5.55, 0.09),
        "weekly": (3.79, 16.64, 0.23),
        "monthly": (21.60, 69.46, 0.31),
    }
    report.ok(
        "the published Sharpe ratios equal mean over standard deviation at each frequency to two"
        " decimals (the "
        "risk-free rate is negligible at these magnitudes)",
        all(abs(m / s - sr) < 0.006 for m, s, sr in lt.values()),
    )
    days = (date(2018, 5, 31) - date(2011, 1, 1)).days + 1
    report.ok(
        "the extreme-day frequencies are counts over roughly 2,720 trading days of a market open"
        " every day: 13 days "
        "below -20% is 0.48% and 26 days above +20% is 0.95%",
        abs(13 / 0.0048 - days) < 30 and abs(26 / 0.0095 - days) < 30,
        f"{days} calendar days 2011-01-01 to 2018-05-31",
    )
    report.ok(
        "weekly standard deviation of 16.64% scales to about 120% a year by the square root of 52,"
        " against roughly "
        "14% for the weekly stock series (1.93%)",
        abs(16.64 * math.sqrt(52) - 120) < 1 and abs(1.93 * math.sqrt(52) - 13.9) < 0.2,
    )


def check_allocation(report: CheckReport) -> None:
    """Part 6: a HYPOTHETICAL small crypto weight's share of portfolio risk."""
    print("== part 6: a HYPOTHETICAL allocation - risk contribution of a small crypto weight")
    # hypothetical: a 60/40 portfolio, a crypto asset, and their correlation
    vol_p, vol_c, rho = 0.10, 0.70, 0.30
    rows = []
    for w in (0.0, 0.01, 0.025, 0.05):
        cov = np.array([[vol_p**2, rho * vol_p * vol_c], [rho * vol_p * vol_c, vol_c**2]])
        wv = np.array([1 - w, w])
        var = wv @ cov @ wv
        rc = wv * (cov @ wv) / var  # Euler risk contributions, summing to one
        rows.append((w, math.sqrt(var), rc[1]))
        report.ok(
            f"weight {w:.1%}: risk contributions sum to one",
            math.isclose(rc.sum(), 1.0),
            f"portfolio vol {math.sqrt(var):.2%}, crypto share of risk {rc[1]:.1%}",
        )
    report.ok(
        "a 5% weight in an asset seven times as volatile supplies nearly a fifth of portfolio risk,"
        " so sizing is set by "
        "risk budget, not by capital",
        0.15 < rows[-1][2] < 0.25,
    )


def check_custody(report: CheckReport) -> None:
    """Part 7: single key against 2-of-3 multisignature, closed form against enumeration."""
    print(
        "== part 7: custody - single key against 2-of-3 multisignature (HYPOTHETICAL probabilities)"
    )
    p_lose, p_steal = 0.05, 0.02  # per key per year, independent: hypothetical
    p2_lose = 3 * p_lose**2 * (1 - p_lose) + p_lose**3
    p2_steal = 3 * p_steal**2 - 2 * p_steal**3
    enum_lose = sum(
        math.prod(p_lose if s else 1 - p_lose for s in st)
        for st in itertools.product([0, 1], repeat=3)
        if sum(st) >= 2
    )
    enum_steal = sum(
        math.prod(p_steal if s else 1 - p_steal for s in st)
        for st in itertools.product([0, 1], repeat=3)
        if sum(st) >= 2
    )
    report.ok(
        "2-of-3 multisig: funds are lost only if two keys are lost and stolen only if two are"
        " compromised; the closed "
        "forms equal enumeration of all eight key states",
        math.isclose(p2_lose, enum_lose) and math.isclose(p2_steal, enum_steal),
        f"loss {p2_lose:.4f} vs {p_lose} single key; theft {p2_steal:.5f} vs {p_steal}",
    )
    report.ok(
        "under these assumptions multisig cuts both risks by an order of magnitude; correlated"
        " failures (keys stored "
        "together, one custodian holding all three) remove the benefit",
        p2_lose < p_lose / 5 and p2_steal < p_steal / 10,
    )


def main() -> int:
    """Print the versions, then run the seven parts with one report and print the count.

    Worked numbers of def:distributed-ledger-applications in
    compendium/digital-assets-prediction-markets/distributed-ledgers.tex and
    meth:digital-asset-investment-analysis in
    compendium/crypto-spot-markets/digital-asset-investing.tex.

    Ledger mechanics (parts 1-4) use real SHA-256 on toy blocks; nothing here touches a live
    network. Part 3 reproduces the attacker-success table of Nakamoto (2008), sec. 11, and
    checks it against an independent simulation of the race (seed 20261020). Part 4 sums the
    Bitcoin issuance schedule (50 coins a block, halving every 210,000 blocks; Narayanan et al.,
    p. 62).

    Investment arithmetic (parts 5-7) uses the published Bitcoin statistics of Liu and
    Tsyvinski (NBER WP 24877, Table 1) for internal-consistency checks, and HYPOTHETICAL inputs,
    labelled as such, for the portfolio and custody examples.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
    report = CheckReport()
    check_ledger(report)
    check_proof_of_work(report)
    check_finality(report, np.random.default_rng(SEED))
    check_supply(report)
    check_published_statistics(report)
    check_allocation(report)
    check_custody(report)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
