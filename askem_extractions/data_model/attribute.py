from pathlib import Path
from typing import Optional, Union, List

import pydantic
from pydantic import BaseModel
from enum import Enum

from . import Equation
from . import AnchoredExtraction
from . import DocumentCollection
from . import FNReference
from . import ScenarioContext


class AttributeType(str, Enum):
    anchored_extraction = "anchored_extraction"
    document_collection = "document_collection"
    equation = "equation"
    fn_reference = "fn_reference"
    scenario_context = "scenario_context"


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
    FNReference,
    ScenarioContext]

    class Config:
        use_enum_value = True
        schema_extra = {
            '$id': "#/definitions/Attribute"
        }

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class AttributeCollection(BaseModel):
    """ Represents a collection of attributes """
    attributes: List[Attribute]

    class Config:
        schema_extra = {
            '$id': "#/definitions/AttributeCollection"
        }

    def save_json(self, path: Union[Path, str], **kwargs):
        """ Saves the collection to a json file """
        path = Path(path)
        with path.open('w') as f:
            f.write(self.json(indent=2, **kwargs))

    @classmethod
    def from_json(cls, path: Union[Path, str]):
        """ Restores a collection from a json file """
        return pydantic.parse_file_as(path=str(path), type_=cls)

    def __hash__(self):
        return hash(tuple(self.attributes))