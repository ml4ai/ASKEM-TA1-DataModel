from typing import Optional

from pydantic import BaseModel

class Dataset(BaseModel):
    """ Represents a dataset """
    id: str
    name: str
    metadata: Optional[str] # Any additional metadata goes as a serialized string here

    class Config:
        schema_extra = {
            '$id': "#/definitions/Dataset"
        }
