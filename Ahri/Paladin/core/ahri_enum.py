import enum
import sys

if sys.version_info < (3, 11):

    class StrEnum(str, enum.Enum):
        def __new__(cls, value):
            if not isinstance(value, str):
                raise TypeError(f"{value!r} is not a string")
            obj = str.__new__(cls, value)
            obj._value_ = value
            return obj

        def __str__(self):
            return self.value

        def __eq__(self, other):
            if isinstance(other, str):
                return self.value == other
            return super().__eq__(other)

    enum.StrEnum = StrEnum
