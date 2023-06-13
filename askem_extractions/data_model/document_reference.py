from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID


class DocumentReference(BaseModel):
    """ Represents a paper from which an extraction comes """
    id:             ID
    source_file:    str
    doi:            str  # Consider making this an instance of a model class too

    class Config:
        schema_extra = {
            '$id': "#/definitions/DocumentReference"
        }

