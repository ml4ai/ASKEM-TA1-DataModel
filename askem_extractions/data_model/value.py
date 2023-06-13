from typing import Optional, List

from pydantic import BaseModel

from askem_extractions.data_model.grounding import Grounding
from askem_extractions.data_model.text_extraction import TextExtraction


class Value(BaseModel):
    source: str  # the text span containing a value
    grounding: Optional[List[Grounding]] # Grounding for the type of the value
    extraction_source: Optional[TextExtraction]

    class Config:
        schema_extra = {
            '$id': "#/definitions/Value"
        }

