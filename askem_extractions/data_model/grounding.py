from typing import List

from pydantic import BaseModel

from askem_extractions.data_model import ID
from askem_extractions.data_model.provenance import Provenance


class Grounding(BaseModel):
    """
    Grounding enables associating a DKG concept identifier with an extraction, along with what information was
    used as the basis for inferring a grounding (through the source list), what algorithm was used for the inference
    (through provenance), and a score estimating the confidence in the grounding (to be used for ranking among
    candidate groundings).

    There are a couple of different types of elements that may be grounded (this list might be expanded in the
    future) – current:

        - AnchoredExtraction: grounding may be based on the Name(s) and/or Description(s) of the AnchoredExtraction.
         In this case, the source list contains the IDs for any Name(s) or Description(s) used by the grounding
         algorithm (most likely an embedding-based model; in embedding models, the order of the IDs indicates the order
         in which Name(s) and/or Description(s) string were concatenated for the embedding input). In general, if
         Description(s) are available, those will be used, with Name(s) as a fall-back when there is no Description.

        - Value: Values may be optionally grounded; here the source is the id of the ValueSpec that the Value is a
         member of: ValueSpec.value.

        - Units: Units may be grounded; here the source is the id of the ValueSpec that the Units is a
        member of: ValueSpec.unit.
    """

    grounding_id: str  # DKG grounding identifier
    source: List[ID]   # See the Grounding general comment explaining the different types of elements that may be
                       # grounded and how the source is determined based on the type.
    score: float       # Used as proxy for confidence in grounding, rank sort hypotheses
    provenance: Provenance

    class Config:
        schema_extra = {
            '$id': "#/definitions/Grounding"
        }


