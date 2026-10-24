"""A one-day snapshot of OKX's BTC option listings and open interest."""

import collections
import datetime as dt
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Self

from trading_notes.records import Record
from trading_notes.research.crypto_venues_perpetuals.deribit_options import largest
from trading_notes.research.workflow import WorkflowArguments


class Instrument(Record):
    """An option listing from /api/v5/public/instruments.

    Attributes:
        instId: The instrument, such as BTC-USD-261225-100000-C.
        settleCcy: The settlement currency.
        ctType: "inverse" or "linear".
        ctMult: The contract multiplier, as published.
        ctValCcy: The currency of the contract value.
        expTime: Expiry, milliseconds since the epoch, as published.
    """

    instId: str
    settleCcy: str
    ctType: str
    ctMult: str
    ctValCcy: str
    expTime: str


class Instruments(Record):
    """A saved instruments response.

    Attributes:
        data: The listings.
    """

    data: list[Instrument]


class OpenInterest(Record):
    """An instrument's entry in /api/v5/public/open-interest.

    Attributes:
        instId: The instrument.
        oiUsd: Open interest in US dollars.
        ts: The snapshot time, milliseconds since the epoch.
    """

    instId: str
    oiUsd: float
    ts: int


class OpenInterests(Record):
    """A saved open-interest response.

    Attributes:
        data: The entries.
    """

    data: list[OpenInterest]


class OptionSnapshot(Record):
    """OKX's BTC option listings and open interest at one time.

    Attributes:
        instruments: The listings.
        open_interest: The open-interest entries.
    """

    instruments: list[Instrument]
    open_interest: list[OpenInterest]

    @classmethod
    def read(cls, instruments: Path, open_interest: Path) -> Self:
        """Read the two saved responses."""
        return cls(
            instruments=Instruments.model_validate_json(instruments.read_text()).data,
            open_interest=OpenInterests.model_validate_json(open_interest.read_text()).data,
        )

    def listings(self) -> list[str]:
        """Return the snapshot time, then instruments by contract terms and expiries by type."""
        ins = self.instruments
        stamp = dt.datetime.fromtimestamp(self.open_interest[0].ts / 1000, dt.UTC)
        lines = [f"snapshot time {stamp:%Y-%m-%d %H:%M} UTC; {len(ins)} BTC option instruments"]
        terms = collections.Counter((i.settleCcy, i.ctType, i.ctMult, i.ctValCcy) for i in ins)
        for (settle, ct, mult, val), n in sorted(terms.items()):
            lines.append(f"  settle {settle}, {ct}, multiplier {mult} {val}: {n} instruments")
        for t in ("inverse", "linear"):
            lines.append(f"  {t} expiries: {len({i.expTime for i in ins if i.ctType == t})}")
        return lines

    def concentration(self) -> list[str]:
        """Return open interest in dollars by contract type, by expiry and in the largest ten.

        An entry without a listing counts under contract type "?".
        """
        ou = {x.instId: x.oiUsd for x in self.open_interest}
        tot = sum(ou.values())
        ct_of = {i.instId: i.ctType for i in self.instruments}
        by_type: dict[str, float] = {}
        by_expiry: dict[str, float] = {}
        for inst, usd in ou.items():
            ct = ct_of.get(inst, "?")
            by_type[ct] = by_type.get(ct, 0) + usd
            expiry = inst.replace("_UM", "").split("-")[2]
            by_expiry[expiry] = by_expiry.get(expiry, 0) + usd
        top3 = largest(by_expiry, 3)
        top10 = sorted(ou.items(), key=lambda x: -x[1])[:10]
        return [
            f"open interest USD {tot / 1e9:.3f} bn: "
            + ", ".join(f"{ct} {usd / tot:.1%}" for ct, usd in largest(by_type)),
            "largest expiries: "
            + ", ".join(f"{e} {v / tot:.1%}" for e, v in top3)
            + f" (together {sum(v for _, v in top3) / tot:.1%})",
            f"ten largest instruments hold {sum(v for _, v in top10) / tot:.1%}; largest: "
            + ", ".join(f"{k} {v / tot:.1%}" for k, v in top10[:3]),
        ]


class Arguments(WorkflowArguments):
    """The snapshot's arguments.

    Attributes:
        instruments: The saved instruments response.
        open_interest: The saved open-interest response.
    """

    folder: ClassVar[str] = "crypto-perpetuals"
    instruments: Path
    open_interest: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the OKX option snapshot, for comparison with Deribit's.

    Inputs: OKX public REST API v5, retrieved 2026-10-17 about 11:52 UTC, instruments and
    open interest for instType=OPTION, uly=BTC-USD. Reported: instrument counts by settlement
    currency and contract type, expiries, and open interest (oiUsd) by contract type, by expiry
    and in the ten largest instruments. Descriptive only.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("instruments", type=Path, help="the saved instruments response")
    parser.add_argument("open_interest", type=Path, help="the saved open-interest response")
    args = Arguments.parse(parser, argv)
    snapshot = OptionSnapshot.read(args.instruments, args.open_interest)
    print("\n".join([*snapshot.listings(), *snapshot.concentration()]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
