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
pip install -e ".[all]"
```
### Installation without cloning git repository
If you want to install this module directly, without having to clone the repository locally, you can do so by running:
```shell
pip install git+https://github.com/ml4ai/ASKEM-TA1-DataModel
```

### Uninstallation
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

## Generate JSON Schema
To generate the json schema, we can leverage pydantic to do it automatically using the  following code snippet:
```python
print(ExtractionsCollection.schema_json(indent=2))
```
## Dockerization
A docker container built using this project's docker file will normalize TA-1 participants' proprietary files and merge the product to a single output file.

To build the image use the following command:

```bash
docker build -f Dockerfile -t askem_ta1_datamodel
```

A container created from this file expects to find files `/data/arizona_extractions.json`  and `/data/mit_extractions.json` and will store the output on `/data/ta1_extractions.json`.


The simplest way to run it is by mapping a directory containing both input files to `/data`, for example, the current directory:
```bash
docker run -it --rm -v $(PWD):/data askem_ta1_datamodel
```

Alternatively, a finer grained control of the path names can be achieved by using the command line parameters explicitly:
```bash
docker run -it --rm -v $(PWD):/data askem_ta1_datamodel ./normalize_extractions.sh -a /data/arizona_extractions.json -m /data/mit_extractions.json -o /data/ta1_extractions.json
```
