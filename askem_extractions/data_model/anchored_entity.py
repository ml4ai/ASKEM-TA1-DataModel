from typing import List, Optional

from pydantic import BaseModel

from askem_extractions.data_model import ID, DataColumnReference
from askem_extractions.data_model.text_description import TextDescription
from askem_extractions.data_model.grounding import Grounding
from askem_extractions.data_model.mention import Mention
from askem_extractions.data_model.value_description import ValueDescription


class AnchoredEntity(BaseModel):
    """ Supports associations of various types of reading extractions associated with a "named" concept.
         There could be more than one name for the same element.
    """

    id: ID
    mentions: List[Mention]
    text_description: Optional[List[TextDescription]] = None
    value_descriptions: Optional[List[ValueDescription]] = None
    groundings: Optional[List[Grounding]] = None
    data_columns: Optional[List[DataColumnReference]] = None

    class Config:
        schema_extra = {
            '$id': "#/definitions/AnchoredExtraction"
        }

    def __hash__(self):
        return hash(self.id.id)
