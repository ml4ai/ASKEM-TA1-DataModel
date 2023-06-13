from pydantic import BaseModel
from datetime import datetime


class Provenance(BaseModel):
    """ Represents the origin of a piece of information related to the extractions """
    method: str  # The inference method / algorithm (with version) used to derive data
    # e.g., "MIT-extraction-v3", "SKEMA-TR-v1"
    timestamp: datetime

    class Config:
        schema_extra = {
            '$id': "#/definitions/Provenance"
        }
