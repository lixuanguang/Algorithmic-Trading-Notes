"""Define one pydantic model, so that importing this module runs pydantic's model start-up."""

from pydantic import BaseModel


class Probe(BaseModel):
    """The first model defined in the process, which makes pydantic look for its plugins.

    Attributes:
        value: An unused field.
    """

    value: float = 0.0
