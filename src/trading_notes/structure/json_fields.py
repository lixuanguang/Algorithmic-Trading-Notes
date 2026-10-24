"""Read fields of untrusted JSON objects as typed values, reporting wrong shapes.

`json.loads` returns untyped data. Callers bind it to `object` and narrow it here before
building trusted records, so a malformed record becomes a reported problem and not a
traceback raised later.
"""

from collections.abc import Callable

type JsonObject = dict[str, object]


def as_object(value: object) -> JsonObject | None:
    """Return a JSON object with its string keys, or None for any other value."""
    if not isinstance(value, dict):
        return None
    return {str(key): field for key, field in value.items()}


def as_objects(value: object) -> list[JsonObject] | None:
    """Return a list whose every element is a JSON object, or None otherwise."""
    if not isinstance(value, list):
        return None
    objects: list[JsonObject] = []
    for element in value:
        obj = as_object(element)
        if obj is None:
            return None
        objects.append(obj)
    return objects


def as_strings(value: object) -> tuple[str, ...] | None:
    """Return a list whose every element is a string as a tuple, or None otherwise."""
    if not isinstance(value, list):
        return None
    strings = tuple(element for element in value if isinstance(element, str))
    return strings if len(strings) == len(value) else None


class JsonRecord:
    """One JSON object whose fields are read as typed values.

    A present field of the wrong JSON type is reported once and then read as absent, so
    later checks see a well-typed value. Scalars accept null as absence. A list field is
    either entirely well typed or rejected: its valid elements are not kept, so a partly
    malformed list is never mistaken for a complete one.

    Attributes:
        fields: The object's fields as parsed.
        where: Repository-relative file name that starts every reported problem.
        name: Identifier of the record within the file, or "" for the file's top level.
        problems: The run's problem list, shared with the caller and appended to.
    """

    def __init__(self, fields: JsonObject, where: str, name: str, problems: list[str]) -> None:
        """Wrap a parsed object.

        Args:
            fields: The object's fields.
            where: File name for problems.
            name: Record identifier for problems; "" for the top-level object.
            problems: List that receives each shape problem; it is appended to.
        """
        self.fields = fields
        self.where = where
        self.name = name
        self.problems = problems

    def child(self, fields: JsonObject) -> JsonRecord:
        """Return a nested object, whose problems are reported under this record's name."""
        return JsonRecord(fields, self.where, self.name, self.problems)

    def get(self, field: str) -> object:
        """Return a field's raw value, None when absent."""
        return self.fields.get(field)

    def text(self, field: str, *, required: bool = False) -> str | None:
        """Return a string field; None when absent, null or (reported) not a string."""
        value = self.fields.get(field)
        if isinstance(value, str):
            return value
        if value is not None or required:
            self._invalid(field, "a string")
        return None

    def nested(self, field: str) -> JsonRecord | None:
        """Return an object field; None when absent, null or (reported) not an object.

        The nested record reports under this record's name or, at the top level, its field's.
        """
        value = self.fields.get(field)
        fields = as_object(value)
        if fields is not None:
            return JsonRecord(fields, self.where, self.name or field, self.problems)
        if value is not None:
            self._invalid(field, "an object")
        return None

    def integer(self, field: str) -> int | None:
        """Return an integer field; None when absent, null or (reported) not an integer.

        JSON true and false are not integers here, although Python's bool subclasses int.
        """
        value = self.fields.get(field)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        if value is not None:
            self._invalid(field, "an integer")
        return None

    def texts(
        self, field: str, *, required: bool = False, nullable: bool = False
    ) -> tuple[str, ...]:
        """Return a list-of-strings field, empty when absent or invalid.

        Args:
            field: Field name.
            required: Report the field when it is absent.
            nullable: Read null as an empty list instead of reporting it.

        Returns:
            The strings in order; empty when the field is absent, null or reported.
        """
        return self._list(field, as_strings, "a list of strings", required, nullable) or ()

    def objects(
        self, field: str, *, required: bool = False, nullable: bool = False
    ) -> list[JsonObject]:
        """Return a list-of-objects field, empty when absent or invalid (see `texts`)."""
        return self._list(field, as_objects, "a list of objects", required, nullable) or []

    def _list[T](
        self,
        field: str,
        narrow: Callable[[object], T | None],
        expected: str,
        required: bool,
        nullable: bool,
    ) -> T | None:
        """Narrow a list field, reporting it when it is required, null or ill-typed."""
        if field not in self.fields:
            if required:
                self._invalid(field, expected)
            return None
        value = self.fields[field]
        if value is None and nullable:
            return None
        narrowed = narrow(value)
        if narrowed is None:
            self._invalid(field, expected)
        return narrowed

    def _invalid(self, field: str, expected: str) -> None:
        """Report a field whose value does not have the expected shape."""
        owner = f"`{self.name}` field " if self.name else ""
        self.problems.append(f"{self.where}: {owner}`{field}` must be {expected}")
