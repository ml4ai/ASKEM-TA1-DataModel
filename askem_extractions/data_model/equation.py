from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID
from askem_extractions.data_model.image_extraction import ImageExtraction
from askem_extractions.data_model.provenance import Provenance


class Equation(BaseModel):
    """ The following is generalized to support extraction of an equation from a document or other medium """

    id: ID
    source_text:       Optional[str]  = None               # Raw sequence of characters
    latex:             Optional[str]  = None               # LaTeX representation
    p_mathml:          Optional[str]  = None               # Presentation MathML
    c_mathml:          Optional[str] = None                # Content MathML
    source_image:      Optional[str] = None                # File path to image
    extraction_source: Optional[ImageExtraction] = None
    provenance:        Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/Equation"
        }