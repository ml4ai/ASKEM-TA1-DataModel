from pydantic import BaseModel


class Paper(BaseModel):
    """ Represents a paper from which an extraction comes """
    id: str
    file_directory: str
    doi: str  # Consider making this an instance of a model class too
