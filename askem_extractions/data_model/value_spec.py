from typing import Optional, List, Tuple

from pydantic import BaseModel

from askem_extractions.data_model import ID
from askem_extractions.data_model.bound import Bound
from askem_extractions.data_model.provenance import Provenance
from askem_extractions.data_model.units import Units
from askem_extractions.data_model.value import Value


class ValueSpec(BaseModel):
    """ Value and unit extractions may come as a pair, and since there may be more than one such pair,
        we provide a ValueSpec as a general structure that itself can contain either a Value, a Unit,
        or a paired Value and Unit
    """

    id: ID  # A unique id for this ValueSpec
    value: Optional[Value]
    units: Optional[Units]
    type: Optional[str]  # String representing the (data) type of the value.
    bounds: Optional[List[Tuple[Bound, Bound]]]  # Represents a list (set) of ordered pairs representing the
    # left/lower and right/upper bounds of an interval on an
    # ordered value domain. When there is no value, the assumption is that any value in the domain is acceptable;
    # when a domain has Tuple(s), then the domain is restricted to values within the specified intervals.
    provenance: Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/ValueSpec"
        }
