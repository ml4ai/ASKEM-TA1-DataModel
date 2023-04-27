from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model.provenance import ProvenanceInfo
from askem_extractions.data_model.statement_value import StatementValue
from askem_extractions.data_model.variable import Variable
from askem_extractions.data_model.variable_statement_metadata import VariableStatementMetadata


class VariableStatement(BaseModel):
    """ Represents a statement about a variable """
    id: str
    variable: Variable
    value: Optional[StatementValue]                 # If there is not a statement value, then this will be empty
    metadata: list[VariableStatementMetadata] = []  # Any optional metadata goes here as a one-to-many relationship
    provenance: Optional[ProvenanceInfo]
