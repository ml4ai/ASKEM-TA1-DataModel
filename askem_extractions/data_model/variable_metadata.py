from pydantic import BaseModel


class VariableMetadata(BaseModel):
    """ Represents some metadata about a variable instance """
    type: str  # Non-safe type if this metadata
    value: str  # Metadata contents serialized as a string
