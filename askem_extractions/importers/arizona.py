import json
from pathlib import Path
from typing import Optional

from askem_extractions.data_model import *


def get_dkg_groundings(block) -> list[DKGConcept]:
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
                    DKGConcept(
                        name=name,
                        id=dkg_id,
                        score=score
                    )
                )

    return ret


def get_paper(block) -> Optional[Paper]:
    """ Helper function to extract the paper name from which this variable came from """

    attachments = block.get('attachments', [])
    for att in attachments:
        if type(att) == dict:
            if 'filename' in att:
                return \
                    Paper(
                        id=att['filename'],
                        file_directory=att['filename'],
                        doi=""  # Leave the DOI empty for now
                    )


def build_statement_value(args) -> StatementValue:
    """ Helper function to extract the statement value """
    value, units, tp, grounding = None, None, None, None
    for key, val in args.items():
        if key not in {"context", 'variable'}:
            val = val[0]
            grounding = get_dkg_groundings(val)
            value = val['text']
            if key == "description":
                tp = StatementValueType.Description
            elif key == "value":
                tp = StatementValueType.Value
            elif key == "unit":
                tp = StatementValueType.UnitAndValue
            else:
                tp = StatementValueType.Misc

    return \
        StatementValue(
            value=f"{value}, {units}" if tp == StatementValueType.UnitAndValue else value,
            type=tp,
            get_dkg_groundings=grounding,
        )


def get_scenario_context(block) -> list[VariableStatementMetadata]:
    """ Helper function to return the scenario context as metadata for the variable statement """
    ret = []
    attachments = block.get('attachments', [])
    for att in attachments:
        if type(att) == dict:
            if 'scenarioLocation' in att:
                for location in att['scenarioLocation']:
                    ret.append(
                        # Create the data model instance of the DKG element and its grounding score
                        VariableStatementMetadata(
                            type="scenario_location",
                            value=location
                        )
                    )
            elif 'scenarioTime' in att:
                for time in att['scenarioTime']:
                    ret.append(
                        # Create the data model instance of the DKG element and its grounding score
                        VariableStatementMetadata(
                            type="scenario_time",
                            value=time
                        )
                    )
    return ret


def import_arizona(path: Path) -> ExtractionsCollection:
    with path.open() as f:
        data = json.load(f)

    # Filter out the un necessary data
    events = [d for d in data if d["type"] != "TextBoundMention"]

    collection = []
    # Make each event a variable statement type
    for e in events:
        arguments = e['arguments']
        # Get the unique extraction id for the current event
        event_id = e['id']
        paper = get_paper(e)

        # Create the variable instance for this extraction
        var_data = arguments['variable'][0]
        var_groundings = get_dkg_groundings(var_data)  # Fetch the DKG groundings

        # Create the data model instance of the variable
        var = \
            Variable(
                id=var_data['text'],
                name=var_data['text'],
                dkg_groundings=var_groundings,
                paper=paper
            )

        # Create the statement value instance.
        # Will be a little involved in the case of Arizona's output, so, we will hide the logic in a helper function
        statement_value = build_statement_value(arguments)

        # Put it together as a VariableStatement instance
        var_statement = \
            VariableStatement(
                id=event_id,
                variable=var,
                value=statement_value
            )

        # Throw in some variable statement metadata, just for fun
        one_metadata = \
            VariableStatementMetadata(
                # Will include all the span of the extraction, including variable, statement value and context (an
                # arizona specific construct)
                type="text_span",
                value=e['text']
            )
        var_statement.metadata.append(one_metadata)

        # Throw in more metadata, this time for work: Will add scenario context as metadata elements
        scenario_context_metadata = get_scenario_context(e)
        var_statement.metadata.extend(scenario_context_metadata)

        # Add it to the list
        collection.append(var_statement)

    return ExtractionsCollection(variable_statements=collection)
