from typing import Optional

from pydantic import BaseModel


class Paper(BaseModel):
    """ Represents a paper from which an extraction comes """
    id: str
    name: str
    md5: Optional[str]
    file_directory: Optional[str]
    doi: str  # Consider making this an instance of a model class too

    class Config:
        schema_extra = {
            '$id': "#/definitions/Paper"
        }

