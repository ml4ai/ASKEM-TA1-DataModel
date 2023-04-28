from typing import Optional

from pydantic import BaseModel


class DKGConcept(BaseModel):
    """ Represents a grounding to a DKG concept """
    id: str
    name: str
    score: Optional[float]

    class Config:
        schema_extra = {
            '$id': "#/definitions/DKGConcept"
        }
