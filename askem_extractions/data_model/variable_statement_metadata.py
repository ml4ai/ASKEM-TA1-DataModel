from pydantic import BaseModel


class VariableStatementMetadata(BaseModel):
    """ Metadata associated to a specific variable statement """
    type: str  # Non-safe type if this metadata
    value: str  # Metadata contents serialized as a string
