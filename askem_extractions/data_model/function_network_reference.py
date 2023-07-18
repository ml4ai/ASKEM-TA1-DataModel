from typing import List

from pydantic import BaseModel


class FNReference(BaseModel):
    """
        Reference to one or more FN Paths in a Gromet Function Network Module Collection
        The HMI does not need to resolve these, but these can be used by SKEMA to reach
        back to source FN structure(s) (and source code).
    """

    paths: List[str]  = None # Each string represent a FN Path
    source_file: str  # File path to GrometFNModuleCollection JSON file

    class Config:
        schema_extra = {
            '$id': "#/definitions/FNReference"
        }
