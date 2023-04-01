from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model.dkg_concept import DKGConcept
from askem_extractions.data_model.statement_value_type import StatementValueType


class StatementValue(BaseModel):
    """ Represents the contents of a statement about a variable """
    value: str                                   # Can be either numeric or a string or a tuple with both
    type: StatementValueType                     # The type of the statement (see the enum for different types)
    dkg_grounding: Optional[DKGConcept]          # Optional grounding of the statement to a DKG Concept
