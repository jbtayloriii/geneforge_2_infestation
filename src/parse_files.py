"""Main script for regenerating Geneforge data."""

import dataclasses
import json
import os
import re
import sys

from absl import app
from absl import flags

from src.parsers import dialog_parser
from src.parsers import scen_data_parser

_GENEFORGE_VERSION_FLAG = flags.DEFINE_enum(
    "geneforge_version", "5", ["5", "2_remake"], "The Geneforge version to parse"
)

_ZONE_DIALOG_MATCHER = re.compile(r"^z\d+[A-Za-z0-9]+dlg\.txt$")
_ZONE_MATCHER = re.compile(r"^z\d+[A-Za-z0-9]+\.txt$")


@dataclasses.dataclass
class GeneforgeFiles:
    """Contains paths to all relevant Geneforge files for parsing."""
    base_folder: str
    scenario_data_filepath: str
    executable_filepath: str

    # Script folder contents
    zone_filepaths: list[str]
    zone_dialog_filepaths: list[str]
    other_script_filepaths: list[str]

def main(argv):
    gf_files = get_geneforge_files(_GENEFORGE_VERSION_FLAG.value)

    # Test parsing a single dialog filepath
    # for dialog_filepath in gf_files.zone_dialog_filepaths[:1]:
    #     parsed_nodes = dialog_parser.parse_dialog(dialog_filepath)


    # Test parsing the scenario data file
    parsed_zones = scen_data_parser.parse_scen_data(gf_files.scenario_data_filepath, len(gf_files.zone_dialog_filepaths))

def get_geneforge_files(version) -> GeneforgeFiles:
    # TODO: make this a real function
    with open("src/file_locations.json", "r") as f:
        file_obj = json.loads(f.read())
    base_folder_prefix = file_obj[version]["base_path"]
    scne_data_filename = file_obj[version]["scen_data_filename"]
    scripts_folder = file_obj[version]["scripts_folder"]

    scripts_folder = os.path.join(base_folder_prefix, scripts_folder)
    other_filepaths = []
    zone_filepaths = []
    zone_dialog_filepaths = []
    for root, dirs, files in os.walk(scripts_folder):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            if (_ZONE_DIALOG_MATCHER.match(filename)):
                zone_dialog_filepaths.append(filepath)
            elif (_ZONE_MATCHER.match(filename)):
                zone_filepaths.append(filename)
            else:
                other_filepaths.append(filename)
            

    return GeneforgeFiles(
        base_folder=base_folder_prefix,
        scenario_data_filepath=os.path.join(base_folder_prefix, scne_data_filename),
        executable_filepath=os.path.join(base_folder_prefix, "MacOS", "Geneforge 2 - Infestation"),
        zone_filepaths=zone_filepaths,
        zone_dialog_filepaths=zone_dialog_filepaths,
        other_script_filepaths=other_filepaths,
    )


if __name__ == "__main__":
    app.run(main)
