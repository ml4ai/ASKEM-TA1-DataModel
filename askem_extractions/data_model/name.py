from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID, DocumentReference
from askem_extractions.data_model.provenance import Provenance
from askem_extractions.data_model.text_extraction import TextExtraction


class Name(BaseModel):
    """ A "named" concept """
    id: ID  # The unique id for this name
    name: str
    extraction_source: Optional[TextExtraction]
    document_reference: Optional[DocumentReference]
    provenance: Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/Name"
        }
