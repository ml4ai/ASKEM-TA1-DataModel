from itertools import tee, filterfalse
from typing import Iterable

from ..data_model import Attribute, AttributeType, AttributeCollection


def categorize_attributes(iterable: AttributeCollection):
    extractions, documents, context = [], [], []
    for i in iterable.attributes:
        if i.type == AttributeType.anchored_extraction:
            extractions.append(i)
        elif i.type == AttributeType.document_collection:
            documents.append(i)
        elif i.type == AttributeType.scenario_context:
            context.append(i)

    return extractions, documents, context


from .arizona import import_arizona
from .mit import import_mit

__all__ = ["import_arizona", "import_mit", "categorize_attributes"]
