from pydantic import BaseModel


class ProvenanceInfo(BaseModel):
    """ Describes the provenance of an extraction """

    method: str           # Pipeline used to generate this extraction. I.e. MIT or SKEMA reading pipelines or others
    description: str      # Arbitrary value used to describe in detail the provenance field
