from typing import Optional, List

from pydantic import BaseModel

from askem_extractions.data_model.grounding import Grounding
from askem_extractions.data_model.text_extraction import TextExtraction


class Value(BaseModel):
    amount: str  # the text span containing a value
    grounding: Optional[List[Grounding]]  = None # Grounding for the type of the value
    extraction_source: Optional[TextExtraction]  = None

    class Config:
        schema_extra = {
            '$id': "#/definitions/Value"
        }

