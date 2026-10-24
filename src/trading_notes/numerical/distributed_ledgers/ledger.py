"""Toy hash-chained blocks, Merkle trees, proof of work and Nakamoto's double-spend race."""

import hashlib
import math
from collections.abc import Sequence
from typing import Self

import numpy as np

from trading_notes.numerical.records import Record

GENESIS_LINK = "0" * 64


def h(data: bytes) -> str:
    """Return the SHA-256 hex digest of data."""
    return hashlib.sha256(data).hexdigest()


def _parent_level(level: list[str]) -> list[str]:
    """Return the hashes one level up, duplicating the last hash when the count is odd."""
    if len(level) % 2:
        level = [*level, level[-1]]
    return [h((level[i] + level[i + 1]).encode()) for i in range(0, len(level), 2)]


class MerkleTree(Record):
    """The Merkle tree of a block's transactions, hashed as UTF-8 strings.

    Attributes:
        transactions: The transactions, in order.
    """

    transactions: tuple[str, ...]

    @property
    def root(self) -> str:
        """Return the Merkle root."""
        level = [h(t.encode()) for t in self.transactions]
        while len(level) > 1:
            level = _parent_level(level)
        return level[0]

    def branch(self, idx: int) -> MerkleBranch:
        """Return transaction idx's Merkle branch."""
        level = [h(t.encode()) for t in self.transactions]
        branch: list[tuple[str, bool]] = []
        while len(level) > 1:
            if len(level) % 2:
                level.append(level[-1])
            sib = idx ^ 1
            branch.append((level[sib], sib < idx))
            level = _parent_level(level)
            idx //= 2
        return MerkleBranch(steps=tuple(branch))


class MerkleBranch(Record):
    """The sibling hashes from a leaf up to the root, as a light client receives them.

    Attributes:
        steps: (sibling hash, sibling is on the left), leaf level first.
    """

    steps: tuple[tuple[str, bool], ...]

    def verifies(self, tx: str, root: str) -> bool:
        """Return whether the transaction hashes up the branch to the root."""
        x = h(tx.encode())
        for sib, left in self.steps:
            x = h((sib + x).encode()) if left else h((x + sib).encode())
        return x == root


class Block(Record):
    """A toy block whose header is the previous block's hash followed by its Merkle root.

    Attributes:
        txs: Its transactions.
        prev: The previous block's hash, as stored in the header.
        digest: The hash of its header (prev + Merkle root).
    """

    txs: tuple[str, ...]
    prev: str
    digest: str

    @classmethod
    def linked(cls, txs: Sequence[str], prev: str) -> Self:
        """Return the block of the transactions linked to the block whose hash is prev."""
        header = prev + MerkleTree(transactions=tuple(txs)).root
        return cls(txs=tuple(txs), prev=header[:64], digest=h(header.encode()))

    def with_transaction(self, i: int, tx: str) -> Self:
        """Return a copy with transaction i replaced and the stored hashes left as they were."""
        txs = list(self.txs)
        txs[i] = tx
        return self.model_copy(update={"txs": tuple(txs)})


class BlockChain(Record):
    """Blocks in order from the first, which links to the all-zero hash.

    Attributes:
        blocks: The blocks.
    """

    blocks: tuple[Block, ...]

    @classmethod
    def of(cls, transactions: Sequence[Sequence[str]]) -> Self:
        """Return the chain of blocks holding each group of transactions, linked in order."""
        blocks: list[Block] = []
        prev = GENESIS_LINK
        for txs in transactions:
            blocks.append(Block.linked(txs, prev))
            prev = blocks[-1].digest
        return cls(blocks=tuple(blocks))

    def valid(self) -> bool:
        """Return whether every block's link and stored hash match its contents."""
        p = GENESIS_LINK
        for b in self.blocks:
            root = MerkleTree(transactions=b.txs).root
            if b.prev != p or h((b.prev + root).encode()) != b.digest:
                return False
            p = b.digest
        return True


class ProofOfWork(Record):
    """A hash target of a number of leading zero bits.

    Attributes:
        bits: The leading zero bits required of a header's hash.
    """

    bits: int

    @property
    def target(self) -> int:
        """Return 2^(256 - bits); a hash must fall below it."""
        return 1 << (256 - self.bits)

    def meets(self, header: str, nonce: int) -> bool:
        """Return whether one hash of the header and nonce falls below the target."""
        return int(h(f"{header}{nonce}".encode()), 16) < self.target

    def mine(self, header: str) -> int:
        """Return the first nonce whose hash with the header falls below the target."""
        nonce = 0
        while not self.meets(header, nonce):
            nonce += 1
        return nonce


class DoubleSpendRace(Record):
    """An attacker with a share q of the hashing power racing an honest chain (sec. 11).

    Attributes:
        attacker: q, the attacker's share; the honest share is p = 1 - q.
    """

    attacker: float

    def poisson_success(self, z: int) -> float:
        """Return the white paper's probability that an attacker z blocks behind catches up."""
        q = self.attacker
        p = 1.0 - q
        lam = z * q / p
        s = 1.0
        for k in range(z + 1):
            poisson = (
                math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))
                if lam > 0
                else float(k == 0)
            )
            s -= poisson * (1 - (q / p) ** (z - k))
        return s

    def exact_success(self, z: int) -> float:
        """Return the probability that the attacker catches up, by the negative-binomial sum.

        The attacker's block count while the honest chain finds z blocks is negative binomial,
        not Poisson; each count is weighted by the catch-up probability min(1, (q/p)^(z-k)).
        """
        q = self.attacker
        p = 1.0 - q
        return sum(
            math.comb(k + z - 1, k) * p**z * q**k * (1.0 if k >= z else (q / p) ** (z - k))
            for k in range(z + 400)
        )

    def simulate(
        self, rng: np.random.Generator, z: int, n: int = 200_000, horizon: int = 400
    ) -> float:
        """Return the simulated probability that the attacker catches up, over n races.

        The attacker's progress while the honest chain finds z blocks is a negative-binomial
        draw; from a remaining deficit the race is a random walk cut off after `horizon` steps.
        """
        q = self.attacker
        k = rng.negative_binomial(z, 1 - q, n)
        deficit = z - k
        caught = deficit <= 0
        d = deficit[~caught].astype(float)
        steps = np.where(rng.random((len(d), horizon)) < q, -1, 1)
        path = d[:, None] + np.cumsum(steps, axis=1)
        caught_later = (path <= 0).any(axis=1)
        return float((caught.sum() + caught_later.sum()) / n)
