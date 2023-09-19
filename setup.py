import os
from setuptools import setup
from pathlib import Path

# Load the readme file
with Path("README.md").open() as f:
    readme = f.read()

setup(
    name="askem_extractions",
    python_requires=">=3.8",
    packages=["askem_extractions.data_model", "askem_extractions.importers"],
    version="2.2.0",
    keywords=["askem", "data model", "extractions", "parameters", "equations"],
    description="ASKEM extractions data model library",
    long_description=readme,
    long_description_content_type="text/markdown",
    # url=info.repo,
    # download_url=info.download_url,
    author=" and ".join(("Enrique Noriega-Atala", )), # TODO Add Chunwei's name and other contrinutors' too
    author_email="enoriega@arizona.edu",
    # license=info.license,
    # see https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

    scripts=[
        os.path.join("examples", "usage.py")
    ],

    install_requires=["pydantic>=2.0.3 "],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
    ],
    # tests_require=test_deps,
    # extras_require={
    #     "test": test_deps,
    #     "all": dev_deps
    # },
    include_package_data=True,
    zip_safe=True,
)