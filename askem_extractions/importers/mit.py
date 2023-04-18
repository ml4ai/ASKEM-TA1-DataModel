import json
from pathlib import Path

from askem_extractions.data_model import ExtractionsCollection, DKGConcept, Dataset, DataColumn, Variable, \
    VariableStatement, VariableMetadata, Paper


def import_mit_and_merge(a_path: Path, m_path: Path, map_path: Path) -> ExtractionsCollection:
    # Extract the data from json file
    from_json = ExtractionsCollection.from_json(a_path)

    with open(m_path, "r") as file_a:
        data_m = json.load(file_a)

    # Load mapping file
    with open(map_path, "r") as mapping_file:
        mappings = mapping_file.readlines()

    # Parse the mappings into a dictionary
    mapping_dict = {}
    for mapping in mappings:
        key, value = mapping.strip().split(": ")
        mapping_dict[key] = value.strip('"').strip(",")

    for vs in from_json.variable_statements:
        entry_b_id = vs.id
        print(entry_b_id)
        if entry_b_id in mapping_dict.values():
            print("Found mapping")
            # Get the corresponding key (id from data_a) and find the entry in data_a
            entry_a_id = [k for k, v in mapping_dict.items() if v == entry_b_id][0]
            for entry_a in data_m:
                if entry_a["id"] == entry_a_id:
                    vs.variable.metadata = entry_a["name"]+": "+' '.join(entry_a["text_annotations"])
                    # if entry_a["dkg_annotations"] is not empty
                    if entry_a["dkg_annotations"]:
                        # iterate through the list of dkg_annotations
                        for term in entry_a["dkg_annotations"]:
                            if len(term)<2:
                                continue
                            dkg = DKGConcept(
                                name=term[1],
                                id=term[0],
                            )
                            vs.variable.dkg_groundings.append(dkg)
                    # if entry_a["data_annotations"] is empty
                    if entry_a["data_annotations"]:
                        # iterate through the list of data_annotations
                        for term in entry_a["data_annotations"]:
                            dataset = Dataset(
                                name=term[0][3],
                                id=term[0][2],
                                metadata=term[1],
                            )
                            column = DataColumn(
                                name=term[0][1],
                                id=str(term[0][2])+"-"+str(term[0][0]),
                                dataset=dataset,
                            )
                            vs.variable.column.append(column)
                    # if entry_a["equation_annotations"] is empty
    from_json.save_json("TA1-integration.json")



def import_mit(m_path: Path) -> ExtractionsCollection:
    collection = []

    with open(m_path, "r") as file_a:
        data_m = json.load(file_a)

    for entry_a in data_m:
        id = entry_a["id"]
        name = entry_a["name"]
        text_annotations = entry_a["text_annotations"]
        dkg_groundings = []
        metadata = []
        # if entry_a["dkg_annotations"] is not empty
        if entry_a["dkg_annotations"]:
            # iterate through the list of dkg_annotations
            for term in entry_a["dkg_annotations"]:
                if len(term) < 2:
                    continue
                dkg = DKGConcept(
                    name=term[1],
                    id=term[0],
                )
                dkg_groundings.append(dkg)
        columns = []
        # if entry_a["data_annotations"] is empty
        if entry_a["data_annotations"]:
            # iterate through the list of data_annotations
            for term in entry_a["data_annotations"]:
                dataset = Dataset(
                    name=term[0][1],
                    id=term[0][0],
                    metadata=term[1],
                )
                col = DataColumn(
                    name=term[0][3],
                    id=str(term[0][0]) + "-" + str(term[0][2]),
                    dataset=dataset,
                )
                columns.append(col)
        # if text_annotations is not empty
        if text_annotations:
            for term in text_annotations:
                md = VariableMetadata(
                    type="text_annotation",
                    value=term,
                )
                metadata.append(md)

        paper = Paper(
            id=entry_a["title"],
            file_directory=entry_a["url"],
            doi=entry_a["doi"],
        )

        variable = Variable(
            id=id,
            name=name,
            metadata=metadata,
            dkg_groundings=dkg_groundings,
            column=columns,
            paper=paper,
        )
        variable_statement = VariableStatement(
            id=id,
            variable=variable,
        )
        collection.append(variable_statement)

    return ExtractionsCollection(variable_statements=collection)


def merge_collections(a_collection: ExtractionsCollection, m_collection: ExtractionsCollection, map_path: Path) -> ExtractionsCollection:
    # Extract the data from json file
    # Load mapping file
    with open(map_path, "r") as mapping_file:
        mappings = mapping_file.readlines()

    # Parse the mappings into a dictionary
    mapping_dict = {}
    for mapping in mappings:
        key, value = mapping.strip().split(": ")
        mapping_dict[key] = value.strip('"').strip(",")

    for vs in a_collection.variable_statements:
        entry_b_id = vs.id
        print(entry_b_id)
        if entry_b_id in mapping_dict.values():
            print("Found mapping")
            # Get the corresponding key (id from data_a) and find the entry in data_a
            entry_a_id = [k for k, v in mapping_dict.items() if v == entry_b_id][0]
            for entry_a in m_collection.variable_statements:
                if entry_a.id == entry_a_id:
                    if entry_a.variable.metadata:
                        for md in entry_a.variable.metadata:
                            md.type = entry_a.variable.name
                            vs.variable.metadata.append(md)
                    # if entry_a.variable.dkg_groundings is not empty
                    if entry_a.variable.dkg_groundings:
                        # iterate through the list of dkg_annotations
                        for term in entry_a.variable.dkg_groundings:
                            vs.variable.dkg_groundings.append(term)
                    # if entry_a.variable.column is not empty
                    if entry_a.variable.column:
                        # iterate through the list of data_annotations
                        for term in entry_a.variable.column:
                            vs.variable.column.append(term)
                    # if entry_a["equation_annotations"] is empty
    return ExtractionsCollection(variable_statements=a_collection.variable_statements)


