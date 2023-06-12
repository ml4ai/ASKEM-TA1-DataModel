from pydantic import BaseModel


class ID(BaseModel):
    """ Represents an identifier such as a UUID, hash, or arbitrary string """

    id: str

    class Config:
        schema_extra = {
            '$id': "#/definitions/ID"
        }
