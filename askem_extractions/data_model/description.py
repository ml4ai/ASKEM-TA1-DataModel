from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID
from askem_extractions.data_model.provenance import Provenance
from askem_extractions.data_model.text_extraction import TextExtraction


class Description(BaseModel):
    """ An extraction of a description string to be anchored to name(s) """
    id: ID
    source: str         # TODO clarify the name and purpose of this field
    extraction_source: Optional[TextExtraction]
    provenance: Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/Description"
        }