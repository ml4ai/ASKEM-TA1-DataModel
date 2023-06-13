import json
from datetime import datetime
from pathlib import Path

from askem_extractions.data_model import Dataset, DataColumnReference, AttributeCollection, Grounding, Provenance, \
    DocumentReference, AnchoredExtraction, ID, Name, Description, Attribute, AttributeType, TextExtraction, \
    DocumentCollection
from . import partition


def import_mit_and_merge(a_path: Path, m_path: Path, map_path: Path) -> AttributeCollection:
    mit_provenance = Provenance(
        method="MIT extractor V1.0",  # TODO: Chunwei, please verify this and change it as you need
        timestamp=str(datetime.utcnow())
    )

    # Extract the data from json file
    from_json = AttributeCollection.from_json(a_path)

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

    anchored_extractions = [a.payload for a in from_json]

    for vs in anchored_extractions:

        entry_b_id = vs.id.id
        print(entry_b_id)
        if entry_b_id in mapping_dict.values():
            print("Found mapping")
            # Get the corresponding key (id from data_a) and find the entry in data_a
            entry_a_id = [k for k, v in mapping_dict.items() if v == entry_b_id][0]
            for entry_a in data_m:
                if entry_a["id"] == entry_a_id:
                    # vs.variable.metadata = entry_a["name"]+": "+' '.join(entry_a["text_annotations"]) # TODO find a place to repurpose this
                    # if entry_a["dkg_annotations"] is not empty
                    if entry_a["dkg_annotations"]:
                        # iterate through the list of dkg_annotations
                        for term in entry_a["dkg_annotations"]:
                            if len(term) < 2:
                                continue
                            dkg = Grounding(
                                grounding_text=term[1],
                                grounding_id=term[0],
                                source=[],
                                score=1.,
                                provenance=mit_provenance
                            )
                            vs.groundings.append(dkg)
                    # if entry_a["data_annotations"] is empty
                    if entry_a["data_annotations"]:
                        # iterate through the list of data_annotations
                        for term in entry_a["data_annotations"]:
                            dataset = Dataset(
                                name=term[0][3],
                                id=term[0][2],
                                metadata=term[1],
                            )
                            column = DataColumnReference(
                                name=term[0][1],
                                id=str(term[0][2]) + "-" + str(term[0][0]),
                                dataset=dataset,
                            )
                            vs.data_columns.append(column)
                    # if entry_a["equation_annotations"] is empty
    from_json.save_json("TA1-integration.json")


def import_mit(m_path: Path) -> AttributeCollection:
    extractions = []

    mit_provenance = Provenance(
        method="MIT extractor V1.0 - text, dataset, formula annotation (chunwei@mit.edu)",
        # TODO: Chunwei, please verify this and change it as you need
        timestamp=str(datetime.utcnow())
    )

    with open(m_path, "r") as file_a:
        data_m = json.load(file_a)

    documents = []
    seen_documents = set()

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
                dkg = Grounding(
                    grounding_text=term[1],
                    grounding_id=term[0],
                    source=list(),
                    score=1.,
                    provenance=mit_provenance
                )
                dkg_groundings.append(dkg)
        columns = []
        # if entry_a["data_annotations"] is empty
        if entry_a["data_annotations"]:
            # iterate through the list of data_annotations
            for term in entry_a["data_annotations"]:
                # print(term)
                dataset = Dataset(
                    name=term[0][1],
                    id=ID(id=term[0][0]),
                    metadata=term[1],
                )
                col = DataColumnReference(
                    name=term[0][3],
                    id=ID(id=str(term[0][0]) + "-" + str(term[0][2])),
                    dataset=dataset,
                )
                columns.append(col)
        # if text_annotations is not empty
        # if text_annotations:
        #     mitid = VariableMetadata(
        #         type="mit_id",
        #         value=id,
        #     )
        #     metadata.append(mitid)
        #
        #     mit_extracted = VariableMetadata(
        #         type="mit_extracted_name",
        #         value=name,
        #     )
        #     metadata.append(mit_extracted)
        #
        #     for term in text_annotations:
        #         md = VariableMetadata(
        #             type="mit_annotation",
        #             value=term,
        #         )
        #         metadata.append(md)
        #
        #     mit_extracted = VariableMetadata(
        #         type="extraction_provenance",
        #         value="MIT extractor V1.0",
        #     )
        #     metadata.append(mit_extracted)
        url = ""
        doi = ""
        doc_ref_id = 1
        if "url" in entry_a.keys():
            url = entry_a["url"],
        if "doi" in entry_a.keys():
            doi = entry_a["doi"]
        paper = DocumentReference(
            id=ID(id=doc_ref_id),
            source_file=entry_a["title"],
            doi=doi,
        )

        if doc_ref_id not in seen_documents:
            documents.append(paper)
            seen_documents.add(doc_ref_id)

        # variable = Variable(
        #     id=id,
        #     name=name,
        #     metadata=metadata,
        #     dkg_groundings=dkg_groundings,
        #     column=columns,
        #     paper=paper,
        # )

        descriptions = [Description(
            id=ID(id=id),
            source=d,
            grounding=None,
            extraction_source=None,
            provenance=mit_provenance
        ) for d in text_annotations]

        text_extraction = TextExtraction(
            char_start=0,
            char_end=0,
            document_reference=paper.id
        )

        anchored_extraction = AnchoredExtraction(
            id=ID(id=id),
            names=[Name(
                id=ID(id=id),
                name=name,
                extraction_source=None,
                provenance=mit_provenance
            )],
            descriptions=descriptions,
            value_specs=None,
            groundings=dkg_groundings,
            data_columns=columns,
            text_extraction=text_extraction
        )
        extractions.append(anchored_extraction)

    attributes = [
                     Attribute(
                         type=AttributeType.anchored_extraction,
                         amr_element_id=None,
                         payload=e
                     ) for e in extractions
                 ] + [
                     Attribute(
                         type=AttributeType.document_collection,
                         amr_element_id=None,
                         payload=DocumentCollection(documents=documents)
                     )
                 ]

    return AttributeCollection(attributes=attributes)


def merge_collections(a_collection: AttributeCollection, m_collection: AttributeCollection,
                      map_path: Path) -> AttributeCollection:
    # Extract the data from json file
    # Load mapping file
    with open(map_path, "r") as mapping_file:
        mappings = mapping_file.readlines()

    # Parse the mappings into a dictionary
    mapping_dict = {}
    for mapping in mappings:
        key, value = mapping.strip().split(": ")
        mapping_dict[key] = value.strip('"').strip(",")

    az_anchored_extractions, az_docs = partition(lambda a: isinstance(a.payload, AnchoredExtraction), (a for a in a_collection.attributes))
    mit_anchored_extractions, mit_docs = partition(lambda a: isinstance(a.payload, AnchoredExtraction), (a for a in m_collection.attributes))

    az_docs = az_docs[0]
    mit_docs = mit_docs[0]

    for vs in (a.payload for a in az_anchored_extractions):
        entry_b_id = vs.id.id
        # print(entry_b_id)
        if entry_b_id in mapping_dict.values():
            # print("Found mapping")
            # Get the corresponding key (id from data_a) and find the entry in data_a
            entry_a_id = [k for k, v in mapping_dict.items() if v == entry_b_id][0]

            for entry_a in (a.payload for a in mit_anchored_extractions):
                if entry_a.id.id == entry_a_id:
                    # TODO Figure out what to do with the metadata
                    # if entry_a.variable.metadata:
                    #     for md in entry_a.variable.metadata:
                    #         # md.type = entry_a.variable.name
                    #         vs.variable.metadata.append(md)
                    # if entry_a.variable.dkg_groundings is not empty
                    if entry_a.descriptions:
                        for d in entry_a.descriptions:
                            vs.descriptions.append(d)
                    if entry_a.groundings:
                        # iterate through the list of dkg_annotations
                        for term in entry_a.groundings:
                            vs.groundings.append(term)
                    # if entry_a.variable.column is not empty
                    if entry_a.data_columns:
                        # iterate through the list of data_annotations
                        for term in entry_a.data_columns:
                            if not vs.data_columns:
                                vs.data_columns = list()
                            vs.data_columns.append(term)
                        # if entry_a["equation_annotations"] is empty

    merged_docs = Attribute(type=AttributeType.document_collection, payload=DocumentCollection(documents=az_docs.payload.documents + mit_docs.payload.documents))

    return AttributeCollection(attributes=az_anchored_extractions + [merged_docs])
