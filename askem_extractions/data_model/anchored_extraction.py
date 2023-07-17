from typing import List, Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID, DataColumnReference
from askem_extractions.data_model.description import Description
from askem_extractions.data_model.grounding import Grounding
from askem_extractions.data_model.name import Name
from askem_extractions.data_model.value_spec import ValueSpec


class AnchoredExtraction(BaseModel):
    """ Supports associations of various types of reading extractions associated with a "named" concept.
         There could be more than one name for the same element.
    """

    id: ID
    names: List[Name]
    descriptions: Optional[List[Description]]
    value_specs: Optional[List[ValueSpec]]
    groundings: Optional[List[Grounding]]
    data_columns: Optional[List[DataColumnReference]]

    class Config:
        schema_extra = {
            '$id': "#/definitions/AnchoredExtraction"
        }

    def __hash__(self):
        return hash(self.id.id)
