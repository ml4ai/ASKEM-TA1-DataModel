from typing import Optional, Union

from pydantic import BaseModel
from enum import Enum

from askem_extractions.data_model import Equation
from askem_extractions.data_model.anchored_extraction import AnchoredExtraction
from askem_extractions.data_model.document_collection import DocumentCollection
from askem_extractions.data_model.function_network_reference import FNReference


class AttributeType(str, Enum):
    anchored_extraction = "anchored_extraction"
    document_collection = "document_collection"
    equation = "equation"
    fn_reference = "fn_reference"


class Attribute(BaseModel):
    """
        A top-level generic Attribute container that can be typed
        Attributes are placed in the AMR "metadata" field (a JSON array), and may optional refer
    """

    type: AttributeType
    amr_element_id: Optional[str]  # When present, this means the attribute is associated with an AMR element,
                                   # and the str represents the AMR element id
    payload: Union[AnchoredExtraction,
                   DocumentCollection,
                   Equation,
                   FNReference]

    class Config:
        use_enum_value = True
        schema_extra = {
            '$id': "#/definitions/Attribute"
        }
