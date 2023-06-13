from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID


class TextExtraction(BaseModel):
    """ Represents the origin or a text extraction """
    page: Optional[int]  # Only required in the case of a COSMOS extraction
    block: Optional[int]  # Only required in the case of a COSMOS extraction
    char_start: int
    char_end: int
    document_reference: ID # Id to the document reference

    class Config:
        schema_extra = {
            '$id': "#/definitions/TextExtraction"
        }
