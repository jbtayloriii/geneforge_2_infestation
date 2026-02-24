"""Functions for parsing Geneforge template files (e.g. gf5itemschars.txt)."""
import copy
import dataclasses
import os
import re

import gf_constants

@dataclasses.dataclass(frozen=True)
class TemplateInfo:
    template_type: str
    template_prefix: str
    removed_stats_by_core_stat: dict[str, list[str]]

# TODO: move to json to allow for multiple files
_GF5_TERRAIN_TEMPLATE_INFO = TemplateInfo(
    template_type="terrain",
    template_prefix="tr",
    removed_stats_by_core_stat={
        "tr_terrain_trait": [],
        "tr_graphic_ed_template": [],
        "tr_first_icon_offset_y": [],
        "tr_first_icon_offset_x": [],
    },
)

_GF5_FLOOR_TEMPLATE_INFO = TemplateInfo(
    template_type="floor",
    template_prefix="fl",
    removed_stats_by_core_stat={},
)

_GF5_ITEM_TEMPLATE_INFO = TemplateInfo(
    template_type="item",
    template_prefix="it",
    removed_stats_by_core_stat={
        "it_extra_description": [],
        "it_stats_to_affect": ["it_stats_addition"],
        "it_ability": [],
        "it_pet_stats_to_affect": ["it_pet_stats_addition"],
    },
)

_GF5_CHAR_TEMPLATE_INFO = TemplateInfo(
    template_type="creature",
    template_prefix="cr",
    removed_stats_by_core_stat={
        "cr_graphic_appearadj": [],
        "cr_abil_num": ["cr_abil_level"],
        "cr_start_item": ["cr_start_item_chance"],
        "cr_stain_when_slain": [],        
    },
)


_NEW_TEMPLATE_PATTERN = re.compile(r"begindefine(?P<template_type>[a-zA-Z0-9]+)\s+(?P<template_id>\d+);")
_IMPORT_PATTERN = re.compile(r"^import = (?P<import_id>\d+);")

_ATTRIBUTE_PATTERN = re.compile(r"(?P<attr_name>[a-z]{2}_[a-zA-Z0-9_]+)\s+((?P<attr_sub_val>\d+)\s+)?= (?P<attr_val>[^;]+);")

# TODO: handle multiple games, and all template types for that game
def parse_templates_for_game(game: gf_constants.GeneforgeGame, scripts_folder, output_folder):
    floor_terrain_filepath = os.path.join(scripts_folder, "gf5floorster.txt")
    item_char_filepath = os.path.join(scripts_folder, "gf5itemschars.txt")
    objs_misc_filepath = os.path.join(scripts_folder, "gf5objsmisc.txt")

    terrain_data_by_id = _parse_file(floor_terrain_filepath, _GF5_TERRAIN_TEMPLATE_INFO)
    floor_data_by_id = _parse_file(floor_terrain_filepath, _GF5_FLOOR_TEMPLATE_INFO)
    item_data_by_id = _parse_file(item_char_filepath, _GF5_ITEM_TEMPLATE_INFO)
    char_data_by_id = _parse_file(item_char_filepath, _GF5_CHAR_TEMPLATE_INFO)

    # TODO: objs and abilities

    for vals, id in char_data_by_id.items():
        print(vals)
        print(id)
        print()


def _parse_file(filepath: str, template_info: TemplateInfo):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    template_by_id = {}

    current_id = -1
    current_template_obj = {}
    for line in lines:
        # Remove extra whitespace, and all text after an inline comment
        text = line.strip().split('//')[0]

        # Skip empty lines
        if not text:
            continue

        # Begin new template
        if text.startswith("begindefine"):

            # Save previous object if we have an ID
            if current_id > -1:
                template_by_id[current_id] = current_template_obj

            # Clear out everything if we see a different definition
            template_match = _NEW_TEMPLATE_PATTERN.match(text)
            if not template_match:
                print(f"Unable to match on line {text}")
                continue
            type = template_match.group("template_type")
            id = template_match.group("template_id")

            # If we see a different template type, clear out everything
            if type != template_info.template_type:
                current_id = -1
                current_template_obj = {}
            else:
                # Make a copy to retain attributes
                current_template_obj = copy.deepcopy(current_template_obj)
                current_id = int(id)
            continue
            
        if current_id == -1:
            continue
        
        # Imports
        import_match = _IMPORT_PATTERN.match(text)
        if import_match:
            import_id = int(import_match.group("import_id"))
            if import_id in template_by_id:
                current_template_obj = copy.deepcopy(template_by_id[import_id])
            else:
                print(f"Missing {template_info.template_type} import ID {import_id}")
                current_template_obj = {}
            continue

        # Attributes
        attr_match = _ATTRIBUTE_PATTERN.match(text)
        if attr_match:
            attr_name = attr_match.group("attr_name")
            attr_val = attr_match.group("attr_val").strip('"')
            attr_sub_val = attr_match.group("attr_sub_val")

            # '-1' values can either be stats, or could be deletions
            # If a -1 is tied to a field that would delete other fields then it
            # cannot be a stat and must be a deletion.
            if attr_val == "-1" and attr_name in template_info.removed_stats_by_core_stat:
                for removed_field in template_info.removed_stats_by_core_stat[attr_name] + [attr_name]:
                    if removed_field not in current_template_obj:
                        continue
                    if attr_sub_val:
                        if attr_sub_val in current_template_obj[removed_field]:
                            current_template_obj[removed_field].pop(attr_sub_val)
                            if len(current_template_obj[removed_field]) == 0:
                                current_template_obj.pop(removed_field)
                    else:
                        current_template_obj.pop(removed_field)
                continue

            # Attribute has multiple sub values, e.g. '1' in:
            #   it_stats_addition 1 = 5;
            if attr_sub_val:
                if attr_name not in current_template_obj:
                    current_template_obj[attr_name] = {}
                print(attr_name)
                print(attr_sub_val)
                print(current_template_obj)
                current_template_obj[attr_name][attr_sub_val] = attr_val
            else:
                current_template_obj[attr_name] = attr_val

    return template_by_id
