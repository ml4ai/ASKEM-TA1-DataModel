# ASKEM Extractions Data Model

This module contains the implementation of the TA1 extractions' data model for interoperability between within TA1 and with TA4.

The _Entity-Relation_ diagram with the specification of the model is found [here](https://miro.com/app/board/uXjVMZvPN6o=/).

## Instalation

Clone this repository to your workstation, then install it in a virtual environment:
```shell
pip install ".[all]"
```

If you want to install the package in _development mode_ use instead:
```shell
pip install -e ".[all"
```

### Uninstall
To remove the package from a virtual environment, use:
```shell
pip uninstall askem-extractions
```

## Usage examples
The script in `examples/usage.py` contains an example of how to _import_ extractions from Arizona's text reading pipeline into the data model.
```python
# Import Arizona extractions into our data model
path_to_json = Path(__file__).parent / Path("arizona_output_example.json")
collection = import_arizona(path_to_json)
```

The `ExtractionsCollection` model is able to serialize the extractions to json:
```python
# Save the collection of arizona extractions as the standard json format
collection.save_json("temp.json")
```

And is able to _load from_ previously serialized json files too:
```python
# Reloads the collection from the json file
deserialized = ExtractionsCollection.from_json("temp.json")
```

The model loaded from disk will be equivalent to the one imported from the performer's specific output format:
```python
# Both collections should be equal. Since we are using pydantic, it will do a deep comparison
assert collection == deserialized, "Deserialization didn't work"
```
