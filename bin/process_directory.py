#!/bin/python
import argparse
import itertools as it

from pathlib import Path

from askem_extractions.data_model import AttributeCollection
from askem_extractions.importers import import_arizona, import_mit


def import_extractions(path: Path, importer):
    return importer(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir", default=".")
    parser.add_argument("input_dir")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    input_dir = Path(args.input_dir)

    # Assumption: if file name starts with "extractions_" it is an arizona file
    #             if it starts with "mit_" it is a MIT file.
    #             when a pair of files share the same suffix, they come from the same paper

    # Figure out the pair of files
    arizona, mit = dict(), dict()
    for p in input_dir.iterdir():
        if p.is_file():
            name = str(p.stem)

            tokens = name.split("_", maxsplit=1)
            if len(tokens) == 2:
                prefix, key = tokens
                if prefix == "extractions":
                    arizona[key] = p
                elif prefix == "mit":
                    mit[key] = p
            else:
                # Silently ignore
                pass

    # Now, iterate over all keys and run the aligner
    for key in set(it.chain(arizona.keys(), mit.keys())):
        output_file = output_dir / f"canonical_{key}.json"
        az_file = arizona.get(key)
        mit_file = mit.get(key)
        # Import the specified files
        normalized = list()
        if az_file:
            try:
                normalized.append(import_extractions(Path(az_file), import_arizona))
            except Exception as ex:
                print(f"Problem parsing Arizona extractions file {az_file}: {type(ex)}  {ex}")
        if mit_file:
            try:
                normalized.append(import_extractions(Path(mit_file), import_mit))
            except Exception as ex:
                print(f"Problem parsing MIT extractions file {mit_file}: {type(ex)} {ex}")

        # Merge any collections imported above
        collections = AttributeCollection(
            attributes=list(it.chain.from_iterable(c.attributes for c in normalized)))
        collections.save_json(str(output_file))
        print(f"Saved file {output_file}")
