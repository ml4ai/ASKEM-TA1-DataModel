from pydantic import BaseModel

from askem_extractions.data_model import Dataset
from askem_extractions.data_model.identifier import ID


class DataColumnReference(BaseModel):
    """ Represents a column of a dataset """
    id: ID
    name: str
    dataset: Dataset

    class Config:
        schema_extra = {
            '$id': "#/definitions/DataColumnReference"
        }

