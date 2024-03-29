from typing import Optional, List

from pydantic import BaseModel

from askem_extractions.data_model.grounding import Grounding
from askem_extractions.data_model.text_extraction import TextExtraction


class Units(BaseModel):
    source: str # the text span containing an expression of units
    grounding: Optional[List[Grounding]]  = None  # TODO Should this be a single grounding or an optional list, as the rest
    # of the models, for consistency?
    extraction_source: Optional[TextExtraction]  = None

    class Config:
        schema_extra = {
            '$id': "#/definitions/Units"
        }