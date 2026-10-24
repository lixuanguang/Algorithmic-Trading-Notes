"""A one-day snapshot of Deribit's listed options: settlement, expiries and open interest."""

import collections
import operator
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar

from trading_notes.records import Record
from trading_notes.research.workflow import WorkflowArguments


def largest(totals: dict[str, float], n: int | None = None) -> list[tuple[str, float]]:
    """Return the n largest totals, ties in insertion order, as Counter.most_common orders them."""
    return sorted(totals.items(), key=operator.itemgetter(1), reverse=True)[:n]


class Instrument(Record):
    """An option listing from public/get_instruments.

    Attributes:
        base_currency: The underlying.
        settlement_currency: The currency it settles in.
        instrument_type: "reversed" (inverse, coin-settled) or "linear".
        expiration_timestamp: Expiry, milliseconds since the epoch.
    """

    base_currency: str
    settlement_currency: str
    instrument_type: str
    expiration_timestamp: int

    @property
    def kind(self) -> tuple[str, str, str]:
        """Return (base, settlement currency, instrument type)."""
        return (self.base_currency, self.settlement_currency, self.instrument_type)


class Instruments(Record):
    """A saved public/get_instruments response.

    Attributes:
        result: The listings.
    """

    result: list[Instrument]

    def listings(self, cur: str) -> list[str]:
        """Return a line per (base, settlement, type): instruments, expiries, strikes per expiry.

        Args:
            cur: The currency the response was requested for, which labels each line.
        """
        lines = []
        for (base, settle, typ), n in sorted(
            collections.Counter(x.kind for x in self.result).items()
        ):
            exp = collections.Counter(
                x.expiration_timestamp for x in self.result if x.kind == (base, settle, typ)
            )
            strikes = sorted(v // 2 for v in exp.values())  # a call and a put per strike
            lines.append(
                f"{cur:4s} file: {base:5s} settled in {settle:4s} ({typ:8s}) {n:4d} instruments,"
                f" {len(exp):2d} expiries, "
                f"strikes per expiry median {strikes[len(strikes) // 2]}, max {strikes[-1]}"
            )
        return lines


class BookSummary(Record):
    """An option's entry in public/get_book_summary_by_currency.

    Attributes:
        instrument_name: Underlying-expiry-strike-type, such as BTC-27MAR26-100000-C.
        open_interest: Open interest, in coins.
        estimated_delivery_price: The index price.
    """

    instrument_name: str
    open_interest: float
    estimated_delivery_price: float


class OptionBook(Record):
    """The open interest of one underlying's options in one settlement currency.

    Attributes:
        entries: The options' book summaries, in response order.
    """

    entries: list[BookSummary]

    @property
    def total(self) -> float:
        """Return the total open interest, in coins."""
        return sum(x.open_interest for x in self.entries)

    def top_share(self, k: int) -> float:
        """Return the percentage of open interest in the k instruments with the most."""
        return (
            sum(sorted((x.open_interest for x in self.entries), reverse=True)[:k])
            / self.total
            * 100
        )

    def by_part(self, part: int) -> dict[str, float]:
        """Return the open interest by a part of the name: 1 the expiry, 2 the strike."""
        out: dict[str, float] = {}
        for x in self.entries:
            key = x.instrument_name.split("-")[part]
            out[key] = out.get(key, 0) + x.open_interest
        return out

    def describe(self, base: str, settled: str) -> list[str]:
        """Return the report lines: size, concentration, and the largest expiries and strikes."""
        n, tot = len(self.entries), self.total
        zero = sum(x.open_interest == 0 for x in self.entries)
        spot = self.entries[0].estimated_delivery_price
        expiries = largest(self.by_part(1), 3)
        strikes = largest(self.by_part(2), 5)
        return [
            f"\n{base} options settled in {settled}: {n} instruments, "
            f"open interest {tot:,.1f} BTC, index {spot:,.0f}; zero-OI instruments {zero}",
            f"  share of open interest in top 1% / 5% / 10% of instruments: "
            f"{self.top_share(max(1, n // 100)):.1f}% / {self.top_share(n // 20):.1f}% /"
            f" {self.top_share(n // 10):.1f}%",
            "  largest expiries: " + ", ".join(f"{e} {v / tot * 100:.1f}%" for e, v in expiries),
            "  largest strikes (all expiries): "
            + ", ".join(f"{k} {v / tot * 100:.1f}%" for k, v in strikes),
        ]


class BookSummaries(Record):
    """A saved public/get_book_summary_by_currency response.

    Attributes:
        result: The entries.
    """

    result: list[BookSummary]

    def options_on(self, base: str) -> OptionBook:
        """Return the options on `base`, coin-settled or USDC-settled (base_USDC)."""
        names = (base, base + "_USDC")
        return OptionBook(
            entries=[x for x in self.result if x.instrument_name.split("-")[0] in names]
        )


class Arguments(WorkflowArguments):
    """The snapshot's arguments.

    Attributes:
        source: The folder of saved Deribit API responses.
    """

    folder: ClassVar[str] = "crypto-perpetuals"
    source: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the Deribit option snapshot behind def:crypto-venue-instrument-structure.

    Reads Deribit's public API responses saved on 2026-10-17: public/get_instruments for BTC,
    ETH and USDC options (listing, settlement, instrument type) and
    public/get_book_summary_by_currency for BTC and USDC options (open interest). A snapshot
    of one venue on one day, not a time series.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("source", type=Path, help="folder of saved Deribit responses")
    args = Arguments.parse(parser, argv)
    for cur in ("BTC", "ETH", "USDC"):
        path = args.source / f"instruments_{cur}_option.json"
        print("\n".join(Instruments.model_validate_json(path.read_text()).listings(cur)))
    books = {
        settled: BookSummaries.model_validate_json(
            (args.source / f"book_summary_{cur}_option.json").read_text()
        ).options_on("BTC")
        for cur, settled in (("BTC", "BTC (inverse)"), ("USDC", "USDC (linear)"))
    }
    for settled, book in books.items():
        print("\n".join(book.describe("BTC", settled)))
    inverse, linear = books.values()
    share = linear.total / inverse.total * 100
    print(f"  USDC-settled BTC open interest relative to inverse: {share:.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
