from typing import Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID
from askem_extractions.data_model.image_extraction import ImageExtraction
from askem_extractions.data_model.provenance import Provenance


class Equation(BaseModel):
    """ The following is generalized to support extraction of an equation from a document or other medium """

    id: ID
    source_text:       Optional[str]                # Raw sequence of characters
    latex:             Optional[str]                # LaTeX representation
    p_mathml:          Optional[str]                # Presentation MathML
    c_mathml:          Optional[str]                # Content MathML
    source_image:      Optional[str]                # File path to image
    extraction_source: Optional[ImageExtraction]
    provenance:        Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/Equation"
        }