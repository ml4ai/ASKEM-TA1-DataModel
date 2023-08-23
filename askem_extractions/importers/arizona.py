import json
import logging

from ..data_model import *


def get_dkg_groundings(block) -> List[Grounding]:
    """
    Helper function to create DKGConcept instances from arizona extractions.
    This is specific to any input data format (i.e. Arizona, MIT, etc)
    """

    ret = list()
    attachments = block.get('attachments', [])
    for att in attachments:
        if type(att) == list:
            for dkg in att:
                name, dkg_id, score = [dkg[0][k] for k in ['name', 'id', 'score']]
                ret.append(
                    # Create the data model instance of the DKG element and its grounding score
                    Grounding(
                        source=[],  # TODO: Fix here
                        grounding_text=name,
                        grounding_id=dkg_id,
                        score=score,
                        provenance=Provenance(
                            method="SKEMA-TR-Embedding",
                            timestamp=str(datetime.utcnow())
                        )
                    )
                )

    return ret


def get_document_reference(block) -> Optional[DocumentReference]:
    """ Helper function to extract the paper name from which this variable came from """

    attachments = block.get('attachments', [])
    for att in attachments:
        if type(att) == dict:
            if 'filename' in att:
                return \
                    DocumentReference(
                        id=ID(id=att['filename']),  # TODO update this with the correct field
                        source_file=att['filename'],
                        doi=""  # Leave the DOI empty for now
                    )
    # In case there is document reference as an attribute
    return \
        DocumentReference(
            id=ID(id="N/A"),
            source_file="N/A",
            doi=""
        )


def build_anchored_extraction(event) -> (AnchoredExtraction, DocumentReference):
    """ Helper function to extract the statement value """

    event_id = str(event['id'])
    arguments = event['arguments']

    event_provenance = Provenance(
        method="Skema TR Pipeline rules",
        timestamp=str(datetime.utcnow())
    )

    document_reference = None

    if 'variable' in arguments:
        # Get the unique extraction id for the current event

        document_reference = get_document_reference(event)

        # Create the variable instance for this extraction
        var_data = arguments['variable'][0]
        var_groundings = [g for g in get_dkg_groundings(var_data) if g.score >= 0.75]  # Fetch the DKG groundings

        # Cosmos doc location where this event occurred, if existent
        var_cs_att = get_mention_location(event)
        if var_cs_att:
            var_text_extraction = \
                TextExtraction(
                    page=var_cs_att['pageNum'][0],
                    block=var_cs_att['blockIdx'][0],
                    char_start=var_data['characterStartOffset'],
                    char_end=var_data['characterEndOffset'],
                    document_reference = document_reference.id
                )
        else:
            var_text_extraction = \
                TextExtraction(
                    page=0,
                    block=0,
                    char_start=var_data['characterStartOffset'],
                    char_end=var_data['characterEndOffset'],
                    document_reference=document_reference.id
                )

        # Create the statement value instance.
        # Will be a little involved in the case of Arizona's output, so, we will hide the logic in a helper function

        descriptions, value_specs, data_columns = [], [], []

        for key, val in arguments.items():
            if key not in {"context", 'variable'}:
                val = val[0]

                # Cosmos doc location where this event occurred, if existent
                val_cs_att = get_mention_location(event)
                if val_cs_att:
                    val_text_extraction = \
                        TextExtraction(
                            page=val_cs_att['pageNum'][0],
                            block=val_cs_att['blockIdx'][0],
                            char_start=val['characterStartOffset'],
                            char_end=val['characterEndOffset'],
                            document_reference=document_reference.id
                        )
                else:
                    val_text_extraction = \
                        TextExtraction(
                            page=0,
                            block=0,
                            char_start=val['characterStartOffset'],
                            char_end=val['characterEndOffset'],
                            document_reference=document_reference.id
                        )

                val_groundings = [g for g in get_dkg_groundings(val) if g.score >= 0.75]

                value = val['text']
                if key == "description":
                    d = Description(
                        id=ID(id=val['id']),
                        source=value,
                        grounding=val_groundings,
                        extraction_source=val_text_extraction,
                        provenance=event_provenance
                    )
                    descriptions.append(d)
                elif key == "value":
                    vs = ValueSpec(
                        id=ID(id=val['id']),
                        value=Value(
                            source=value,
                            grounding=val_groundings,
                            extraction_source=val_text_extraction
                        ),
                        units=None,
                        type=None,
                        bounds=None,
                        provenance=event_provenance
                    )
                    value_specs.append(vs)
                elif key == "unit":
                    vs = ValueSpec(
                        id=ID(id=val['id']),
                        value=Value(
                            source=value,
                            grounding=val_groundings,
                            extraction_source=val_text_extraction
                        ),
                        units=None,
                        type=None,
                        bounds=None,
                        provenance=event_provenance
                    )
                    value_specs.append(vs)

        return \
            (AnchoredExtraction(
                   id=ID(id=str(event_id)),
                   names=[Name(
                       id=ID(id=str(var_data['id'])),
                       name=var_data['text'],
                       extraction_source=var_text_extraction,
                       provenance=event_provenance
                   )],
                    descriptions=descriptions,
                    value_specs=value_specs,
                   groundings=var_groundings),
                document_reference)


def get_scenario_context(block) -> List[ScenarioContext]:
    """ Helper function to return the scenario context as metadata for the variable statement """
    ret = []
    attachments = block.get('attachments', [])
    for att in attachments:
        if type(att) == dict:
            if 'scenarioLocation' in att:
                for location in att['scenarioLocation']:
                    ret.append(
                        ScenarioContext(
                            id=ID(id=str(hash("location-"+location))),
                            location = LocationContext(
                                location=location,
                                provenance=Provenance(
                                    method="SKEMA-TR-Context-1.0",
                                    timestamp=str(datetime.utcnow())
                                ),
                                grounding=None
                            )
                        )
                    )
            elif 'scenarioTime' in att:
                for time in att['scenarioTime']:
                    ret.append(
                        ScenarioContext(
                            id = ID(id=str(hash("temporal-time"))),
                            time=TemporalContext(
                                datetime=time,
                                provenance=Provenance(
                                    method="SKEMA-TR-Context-1.0",
                                    timestamp=str(datetime.utcnow())
                                ),
                                grounding=None
                            )
                        )
                    )
    return ret


def get_mention_location(mention):
    attachments = mention['attachments']

    for a in attachments:
        if type(a) == dict:
            if a.get("attType", None) == "MentionLocation":
                return a


def import_arizona(path: Path) -> AttributeCollection:
    with path.open() as f:
        data = json.load(f)
        # If this contains docs plus mentions, keep only the mentions
        if type(data) == dict and 'mentions' in data:
            data = data['mentions']

    # Filter out the un necessary data
    events = [d for d in data if d["type"] != "TextBoundMention"]

    extractions = []
    documents = []
    contexts = []
    seen_documents = set()
    # Make each event a variable statement type
    for e in events:
        try:
            processed = build_anchored_extraction(e)
            if processed:
                anchored_extraction, document_reference = processed

                if document_reference.id.id not in seen_documents:
                    seen_documents.add(document_reference.id.id)
                    documents.append(document_reference)

                # Throw in some variable statement metadata, just for fun
                # one_metadata = \
                #     VariableStatementMetadata(
                #         # Will include all the span of the extraction, including variable, statement value and context (an
                #         # arizona specific construct)
                #         type="text_span",
                #         value=e['text']
                #     )
                # var_statement.metadata.append(one_metadata)

                # Will add scenario context as metadata elements
                scenario_contexts = get_scenario_context(e)
                for sc in scenario_contexts:
                    sc.extractions.append(anchored_extraction.id)

                # Add it to the list
                extractions.append(anchored_extraction)
                contexts.extend(scenario_contexts)
        except Exception as ex:
            print(f"import_arizona error: {ex}")


    attributes = [
        Attribute(
            type=AttributeType.anchored_extraction,
            payload=e
        ) for e in extractions
    ]

    doc_collection = \
        Attribute(
            type=AttributeType.document_collection,
            payload=DocumentCollection(documents=documents)
        )

    contexts = [
        Attribute(
            type=AttributeType.scenario_context,
            payload=c
        ) for c in contexts
    ]

    collection = AttributeCollection(attributes=attributes + contexts + [doc_collection])

    return collection
