from enum import Enum


class StatementValueType(str, Enum):
    """ Represents the type of the statement """
    Description = "description"      # Description or definition of a variable
    Value = "value"                  # Value assignment of a variable
    Unit = "unit"                    # Describes the units that the value may take
    UnitAndValue = "unit_and_value"  # Describes the unit AND the value that may take
    Misc = "misc"                    # Any other unaccounted statement type can use this