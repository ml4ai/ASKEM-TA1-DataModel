from pydantic import BaseModel

from askem_extractions.data_model.dataset import Dataset


class DataColumn(BaseModel):
    """ Represents a column of a dataset """
    id: str
    name: str
    dataset: Dataset
