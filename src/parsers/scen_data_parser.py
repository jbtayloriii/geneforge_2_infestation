"""Parser that handles parsing the binary data file."""

import dataclasses
import io

# Zone sizes
_ZONE_DATA_SIZE = 52088
_ZONE_INITIAL_OFFSET = 2560
FLOOR_OFFSET = 32
terrainoffset = 4128
itemoffset = 12320
objectoffset = 15840
CREATURE_OFFSET = 30176
OBJECT_OFFSET = 15840

@dataclasses.dataclass
class ScenData:
    name: str

def parse_scen_data(scen_data_filepath, zone_count):
    zone_data_list = _get_zones_raw_data(scen_data_filepath, zone_count)

    print(scen_data_filepath)
    for zone_data in zone_data_list[:3]:
        name = _bin_to_str(zone_data[0:19])
        script = _bin_to_str(zone_data[20:31])
        floor_data = _get_floor_data(zone_data)

        for row in floor_data:
            print(row)
        print()

        # print(f"name: {name}, script: {script}")

# 17C38 - z0

def _get_zones_raw_data(scen_data_filepath, zone_count):
    zone_data = []
    with open(scen_data_filepath, "rb") as f:
        for x in range(zone_count):
            f.seek(_ZONE_INITIAL_OFFSET + (_ZONE_DATA_SIZE * x))
            zone_data.append(f.read(_ZONE_DATA_SIZE))

    return zone_data

def _get_floor_data(dataslice):
    floor_map = []
    for x in range(64):
        row = []
        for y in range(64):
            row.append(dataslice[x + FLOOR_OFFSET + (y * 64)])
        floor_map.append(row)
    return floor_map

def _bin_to_str(dataslice):
    bin_str = io.StringIO()
    for val in dataslice:
        if val in range(32, 127):
            bin_str.write(chr(val))
        else:
            break
    return bin_str.getvalue()
