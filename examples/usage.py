"""
    Script with an example of a use case.
    For this script to work, you will have to install the package. See the README
"""

from pathlib import Path

from askem_extractions.data_model import *
from askem_extractions.importers import import_arizona, import_mit
from askem_extractions.importers.mit import merge_collections

if __name__ == "__main__":
    # Import Arizona extractions into our data model
    path_to_json = Path(__file__).parent / Path("arizona_output_example.json")
    a_collection = import_arizona(path_to_json)

    # Save the collection of arizona extractions as the standard json format
    a_collection.save_json("a_temp.json")

    # Reloads the collection from the json file
    deserialized = AttributeCollection.from_json("a_temp.json")

    # Both collections should be equal. Since we are using pydantic, it will do a deep comparison
    assert a_collection == deserialized, "Deserialization didn't work"

    # Print the collection
    print("Arizona Worked!!!")

    # Import MIT extractions into our data model
    path_to_json = Path(__file__).parent / Path("mit_extraction.json")
    m_collection = import_mit(path_to_json)

    # Save the collection of arizona extractions as the standard json format
    m_collection.save_json("m_temp.json")

    # Reloads the collection from the json file
    deserialized = AttributeCollection.from_json("m_temp.json")

    # Both collections should be equal. Since we are using pydantic, it will do a deep comparison
    assert m_collection == deserialized, "Deserialization didn't work"

    # Print the collection
    print("MIT Worked!!!")
    #
    # Merge both data model with the mapping file
    merged = merge_collections(a_collection, m_collection,
                               Path(__file__).parent / Path("mapping.txt"))
    merged.save_json("ta1-bucky_extraction_v1.json")

