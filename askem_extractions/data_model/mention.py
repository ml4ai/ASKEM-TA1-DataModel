from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID
from askem_extractions.data_model.provenance import Provenance
from askem_extractions.data_model.text_extraction import TextExtraction


class Mention(BaseModel):
    """ A "named" concept """
    id: ID  # The unique id for this name
    name: str
    extraction_source: Optional[TextExtraction]  = None
    provenance: Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/Name"
        }
