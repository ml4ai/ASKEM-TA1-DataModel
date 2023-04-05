from typing import Optional

from pydantic import BaseModel


class Equation(BaseModel):
    """ Represents an equation extraction """
    id: str
    text: str               # Text, LaTeX or MathML representation of the formula
    image: Optional[str]    # Optional path or url to an image depicting the formula
