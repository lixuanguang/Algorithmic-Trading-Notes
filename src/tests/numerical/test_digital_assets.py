"""Tests of the toy ledger's Merkle branches, chain links, proof of work and finality."""

# The example's full run is tested in test_checks.py, which checks one branch of a four-leaf
# block. These check every leaf of blocks with one to seven transactions, where odd levels
# duplicate their last hash, and that tampering breaks the chain from the tampered block on.

import math
import unittest

from trading_notes.numerical.distributed_ledgers import digital_assets_checks as da
from trading_notes.numerical.distributed_ledgers.ledger import (
    BlockChain,
    DoubleSpendRace,
    MerkleTree,
    ProofOfWork,
)


class MerkleBranches(unittest.TestCase):
    """Every leaf's branch leads to the root computed separately, for any leaf count."""

    def test_every_leaf_verifies(self) -> None:
        """Branches have ceil(log2 n) hashes and verify their own leaf only."""
        for n in range(1, 8):
            txs = [f"tx {i}" for i in range(n)]
            tree = MerkleTree(transactions=tuple(txs))
            root = tree.root
            for i in range(n):
                with self.subTest(n=n, i=i):
                    branch = tree.branch(i)
                    self.assertEqual(len(branch.steps), math.ceil(math.log2(n)))
                    self.assertTrue(branch.verifies(txs[i], root))
                    self.assertFalse(branch.verifies(txs[i] + "!", root))


class ChainLinks(unittest.TestCase):
    """A block's stored hash covers its transactions and its link to the previous block."""

    def test_tampering_breaks_from_the_tampered_block(self) -> None:
        """Altering block j invalidates every prefix that includes it, and no shorter one."""
        chain = BlockChain.of(da.BLOCKS_TX)
        for j in range(len(chain.blocks)):
            blocks = list(chain.blocks)
            blocks[j] = blocks[j].with_transaction(0, blocks[j].txs[0] + " (altered)")
            with self.subTest(j=j):
                self.assertEqual(
                    [BlockChain(blocks=tuple(blocks[: k + 1])).valid() for k in range(len(blocks))],
                    [k < j for k in range(len(blocks))],
                )
                self.assertTrue(chain.valid())


class Finality(unittest.TestCase):
    """The white paper's Poisson race against the exact negative-binomial race."""

    def test_printed_values_and_certain_catch_up(self) -> None:
        """Q = 0.1, z = 5 gives 0.0009137; an even split is caught up with certainty."""
        race = DoubleSpendRace(attacker=0.1)
        self.assertAlmostEqual(race.poisson_success(5), 0.0009137, places=7)
        self.assertEqual(race.poisson_success(0), 1.0)
        self.assertLess(race.poisson_success(5), race.exact_success(5))
        self.assertAlmostEqual(DoubleSpendRace(attacker=0.5).exact_success(3), 1.0, places=12)


class Work(unittest.TestCase):
    """A mined nonce meets the target, and every smaller nonce misses it."""

    def test_first_nonce_below_target(self) -> None:
        """Mine returns the first nonce whose hash is below 2^(256 - bits)."""
        work = ProofOfWork(bits=8)
        nonce = work.mine("block")
        self.assertTrue(work.meets("block", nonce))
        self.assertFalse(any(work.meets("block", k) for k in range(nonce)))
        self.assertEqual(work.target, 1 << 248)


if __name__ == "__main__":
    unittest.main()
