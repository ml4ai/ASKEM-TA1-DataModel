"""
    Script with an example of a use case.
    For this script to work, you will have to install the package. See the README
"""

from pathlib import Path

from askem_extractions.data_model import *
from askem_extractions.importers import import_arizona, import_mit

if __name__ == "__main__":
    # Import Arizona extractions into our data model
    path_to_json = Path(__file__).parent / Path("arizona_output_example.json")
    collection = import_arizona(path_to_json)

    # Save the collection of arizona extractions as the standard json format
    collection.save_json("temp.json")

    # Reloads the collection from the json file
    deserialized = ExtractionsCollection.from_json("temp.json")

    # Both collections should be equal. Since we are using pydantic, it will do a deep comparison
    assert collection == deserialized, "Deserialization didn't work"

    # Print the collection
    print("Arizona Worked!!!")

    # Import MIT extractions into our data model with the mapping file
    import_mit(Path("temp.json"), Path("mit_extraction.json"),
               Path("mapping.txt"))

