from pydantic import BaseModel

from askem_extractions.data_model.variable import Variable


class Equation(BaseModel):
    """ Represents an equation extraction """
    id: str
    text: str
    variable: list[Variable]