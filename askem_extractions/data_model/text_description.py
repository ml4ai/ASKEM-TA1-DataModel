from typing import Optional, List

from pydantic import BaseModel

from askem_extractions.data_model import ID, Grounding
from askem_extractions.data_model.provenance import Provenance
from askem_extractions.data_model.text_extraction import TextExtraction


class TextDescription(BaseModel):
    """ An extraction of a description string to be anchored to name(s) """
    id: ID
    description: str         # TODO clarify the name and purpose of this field
    grounding: Optional[List[Grounding]]  = None # Grounding for the type of the value
    extraction_source: Optional[TextExtraction] = None
    provenance: Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/Description"
        }