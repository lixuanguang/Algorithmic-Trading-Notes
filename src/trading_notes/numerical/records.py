"""Pydantic base classes for the numerical package's parameter and result records."""

from pydantic import BaseModel, ConfigDict


class Record(BaseModel):
    """An immutable record; NumPy arrays are accepted as field values without conversion."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class MutableRecord(BaseModel):
    """A record whose fields are updated as a computation accumulates results."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
