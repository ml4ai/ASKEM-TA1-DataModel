from typing import Optional, List

from pydantic import BaseModel

from askem_extractions.data_model import Provenance, Grounding, TextExtraction, ID


class LocationContext(BaseModel):

    location: str
    provenance: Provenance
    grounding: Optional[Grounding]  = None
    extraction_source: Optional[TextExtraction]  = None


class TemporalContext(BaseModel):

    datetime: Optional[str]  = None# If it is a single time point, it will go here
    start_datetime: Optional[str]  = None# If it is an interval, this will hold the starting point
    end_datetime: Optional[str]  = None# If it is an interval, this will hold the starting point
    provenance: Provenance
    grounding: Optional[Grounding] = None



class ScenarioContext(BaseModel):
    id: ID
    extractions: List[ID] = [] # just a list of AnchoredExtraction IDs, so don't need to copy whole AEs
    location: Optional[LocationContext]  = None
    time: Optional[TemporalContext]  = None

    def __hash__(self):
        return hash(self.id.id)