"""Main script for regenerating Geneforge data."""

import dataclasses
import json
import os
import re
import sys

from absl import app
from absl import flags

_GENEFORGE_VERSION_FLAG = flags.DEFINE_enum(
    "geneforge_version", "2_remake", ["2_remake"], "The Geneforge version to parse"
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
    print("test")
    gf_files = get_geneforge_files(_GENEFORGE_VERSION_FLAG.value)

    print("Dialog files:")
    for dialog_filepath in gf_files.zone_dialog_filepaths:
        print(dialog_filepath)
    print()

    print("Zone files:")
    for zone_filepath in gf_files.zone_filepaths:
        print(zone_filepath)


    print("Other files:")
    for filepath in gf_files.other_script_filepaths:
        print(filepath)


def get_geneforge_files(version) -> GeneforgeFiles:
    # TODO: make this a real function
    with open("src/file_locations.json", "r") as f:
        file_obj = json.loads(f.read())
    base_folder_prefix = file_obj[version]["base_path"]

    scripts_folder = os.path.join(base_folder_prefix, "Resources", "Scripts")
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
        scenario_data_filepath=os.path.join(base_folder_prefix, "Resources", "GF2ScenData.dat"),
        executable_filepath=os.path.join(base_folder_prefix, "MacOS", "Geneforge 2 - Infestation"),
        zone_filepaths=zone_filepaths,
        zone_dialog_filepaths=zone_dialog_filepaths,
        other_script_filepaths=other_filepaths,
    )


if __name__ == "__main__":
    app.run(main)
