from typing import Optional

from pydantic import BaseModel


class TextExtraction(BaseModel):
    """ Represents the origin or a text extraction """
    page: Optional[int]  # Only required in the case of a COSMOS extraction
    block: Optional[int]  # Only required in the case of a COSMOS extraction
    char_start: int
    char_end: int

    class Config:
        schema_extra = {
            '$id': "#/definitions/TextExtraction"
        }
