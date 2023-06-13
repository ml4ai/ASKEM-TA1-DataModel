from typing import Optional

from pydantic import BaseModel
from enum import Enum


class BoundType(str, Enum):
    closed = 'closed'  # Endpoint is included in the set
    open = 'open'  # Endpoint is not included in the set
    unbounded = 'unbounded'  # The endpoint is effectively infinite


class Bound(BaseModel):
    type: BoundType
    value: Optional[str]  # string representing the bound value
    # if type is "Unbounded", then value is not specified

    class Config:
        schema_extra = {
            '$id': "#/definitions/Bound"
        }