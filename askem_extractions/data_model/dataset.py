from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID


class Dataset(BaseModel):
    """ Represents a dataset """
    id: ID
    name: str
    metadata: Optional[str]  # Any additional metadata goes as a serialized string here

    class Config:
        schema_extra = {
            '$id': "#/definitions/Dataset"
        }