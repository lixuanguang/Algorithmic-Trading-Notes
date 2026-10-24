"""Tests of the toy ledger's Merkle branches and chain links.

The example's full run is tested in test_checks.py, which checks one branch of a four-leaf
block. These check every leaf of blocks with one to seven transactions, where odd levels
duplicate their last hash, and that tampering breaks the chain from the tampered block on.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import math
import unittest
from dataclasses import replace

# project library imports
from trading_notes.numerical import digital_assets as da


class MerkleBranches(unittest.TestCase):
    """Every leaf's branch leads to the root computed separately, for any leaf count."""

    def test_every_leaf_verifies(self) -> None:
        """Branches have ceil(log2 n) hashes and verify their own leaf only."""
        for n in range(1, 8):
            txs = [f"tx {i}" for i in range(n)]
            root = da.merkle_root(txs)
            for i in range(n):
                with self.subTest(n=n, i=i):
                    branch = da.merkle_branch(txs, i)
                    self.assertEqual(len(branch), math.ceil(math.log2(n)))
                    self.assertTrue(da.verify_branch(txs[i], branch, root))
                    self.assertFalse(da.verify_branch(txs[i] + "!", branch, root))


class ChainLinks(unittest.TestCase):
    """A block's stored hash covers its transactions and its link to the previous block."""

    def test_tampering_breaks_from_the_tampered_block(self) -> None:
        """Altering block j invalidates every prefix that includes it, and no shorter one."""
        chain: list[da.Block] = []
        prev = "0" * 64
        for txs in da.BLOCKS_TX:
            header = prev + da.merkle_root(txs)
            prev = da.h(header.encode())
            chain.append(da.Block(list(txs), header[:64], prev))
        for j in range(len(chain)):
            tampered = [replace(b, txs=list(b.txs)) for b in chain]
            tampered[j].txs[0] += " (altered)"
            with self.subTest(j=j):
                self.assertEqual(
                    [da.chain_valid(tampered[: k + 1]) for k in range(len(chain))],
                    [k < j for k in range(len(chain))],
                )
                self.assertTrue(da.chain_valid(chain))


if __name__ == "__main__":
    unittest.main()
