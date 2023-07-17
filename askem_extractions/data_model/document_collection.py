from typing import List

from pydantic import BaseModel

from askem_extractions.data_model import DocumentReference


class DocumentCollection(BaseModel):
    documents: List[DocumentReference]

    class Config:
        schema_extra = {
            '$id': "#/definitions/DocumentCollection"
        }

    def __hash__(self):
        return hash(tuple(self.documents))