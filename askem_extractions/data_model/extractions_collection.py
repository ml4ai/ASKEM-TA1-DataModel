from pathlib import Path
from typing import Union

import pydantic
from pydantic import BaseModel

from askem_extractions.data_model import VariableStatement


class ExtractionsCollection(BaseModel):
    """ Represents a collection of extractions """
    variable_statements: list[VariableStatement]

    def save_json(self, path: Union[Path, str]):
        """ Saves the collection to a json file """
        path = Path(path)
        with path.open('w') as f:
            f.write(self.json())

    @classmethod
    def from_json(cls, path: Union[Path, str]):
        """ Restores a collection from a json file """
        return pydantic.parse_file_as(path=str(path), type_=cls)