from typing import Tuple, Any

from pydantic import BaseModel

from askem_extractions.data_model import ID


class ImageExtraction(BaseModel):
    """ Represents an image extracted by COSMOS or any document processing front-end """

    document_coordinate: Any  # The precise type of this field is yet to be defined
    document_reference: ID

    class Config:
        schema_extra = {
            '$id': "#/definitions/ImageExtraction"
        }
