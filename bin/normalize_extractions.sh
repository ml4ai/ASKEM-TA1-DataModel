#!/bin/bash
# Wrapper to run the normalize_extractions.py script within a docker container

if [ $# -eq 0 ]
then
  python normalize_extractions.py -a /data/arizona_extractions.json -m /data/mit_extractions.json -o /data/ta1_extractions.json;
else
  python normalize_extractions.py "$@";
fi
