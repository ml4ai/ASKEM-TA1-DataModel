import json
from pathlib import Path

from askem_extractions.data_model import ExtractionsCollection, DKGConcept, Dataset, DataColumn


def import_mit(a_path: Path, m_path: Path, map_path: Path) -> ExtractionsCollection:
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
                                name=term[3],
                                id=term[2],
                            )
                            column = DataColumn(
                                name=term[1],
                                id=str(term[2])+"-"+str(term[0]),
                                dataset=dataset,
                            )
                            vs.variable.column.append(column)
                    # if entry_a["equation_annotations"] is empty
    from_json.save_json("TA1-integration.json")


if __name__ == "__main__":
    import_mit(Path("../../examples/temp.json"), Path("../../examples/mit_extraction.json"), Path("../../examples/mapping.txt"))