#!/bin/python
import argparse
import itertools as it

from pathlib import Path

from askem_extractions.data_model import ExtractionsCollection
from askem_extractions.importers import import_arizona, import_mit


def import_extractions(path: Path, importer):
    return importer(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--arizona_input_file")
    parser.add_argument("-m", "--mit_input_file")
    parser.add_argument("-o", "--output_file", default="output_extractions.json")

    args = parser.parse_args()

    if not (args.arizona_input_file or args.mit_input_file):
        print("Should provide at least one input file: Arizona and/or MIT")
        exit(1)

    # Import the specified files
    normalized = list()
    if args.arizona_input_file:
        try:
            normalized.append(import_extractions(Path(args.arizona_input_file), import_arizona))
        except Exception as ex:
            print(f"Problem parsing Arizona extractions file {args.arizona_input_file}: {type(ex)}  {ex}")
    if args.mit_input_file:
        try:
            normalized.append(import_extractions(Path(args.mit_input_file), import_mit))
        except Exception as ex:
            print(f"Problem parsing MIT extractions file {args.mit_input_file}: {type(ex)} {ex}")

    # Merge any collections imported above
    collections = ExtractionsCollection(
        variable_statements=list(it.chain.from_iterable(c.variable_statements for c in normalized)))
    # Compute the output file name
    # new_name = f"canonical_{path_to_json.stem}.json"
    # Save the collection of arizona extractions as the standard json format
    collections.save_json(args.output_file)
