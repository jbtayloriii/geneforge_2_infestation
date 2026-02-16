import scipy.misc
import numpy as np
import os
import constants

import parsers.templateParser as templateParser

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5/Geneforge 5 Files')
GENEFORGE_DATA_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'aGF5ScenData.dat')

GENEFORGE_FLOOR_STER_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'Scripts/gf5floorster.txt')

WIDTH = 64
HEIGHT = 64
CHANNELS = 3

WALL_COLOR = [155, 155, 155]
FLOOR_COLOR = [55, 55, 55]
DOOR_COLOR = [100, 100, 100]
WATER_COLOR = [0, 0, 255]

_PIXEL_PER_COORD = 16

TERRAIN_TEMPLATE_DICT = templateParser.parseTerrain(GENEFORGE_FLOOR_STER_FILE_PATH)

def create_zone_image(terrain_matrix, output_filepath):
	magnification = _PIXEL_PER_COORD
	img = np.zeros((HEIGHT * magnification, WIDTH * magnification, CHANNELS), dtype = np.uint8)

	for y in range(img.shape[0]):
		for x in range(img.shape[1]):
			ter_x = x//magnification
			ter_y = y//magnification

			# position within a square as well as whether there is a wall to the left or below
			is_upper = y % magnification < magnification // 2
			is_right = x % magnification >= magnification // 2
			wall_below = is_wall(ter_x, ter_y + 1, terrain_matrix)
			wall_to_left = is_wall(ter_x - 1, ter_y, terrain_matrix)

			terrain_val = terrain_matrix[ter_y][ter_x]

			terrain = TERRAIN_TEMPLATE_DICT.get(str(terrain_val))
			if terrain is None:
				continue
			if terrain.get('tr_blockage_type1') == '3':
				if is_upper or wall_below:
					if is_right or wall_to_left:
						if is_upper or is_right or is_wall(ter_x - 1, ter_y + 1, terrain_matrix):
							img[y][x] = WALL_COLOR
			if terrain.get('tr_blockage_type1') == '2':
				img[y][x] = WATER_COLOR
	#scipy.misc.imshow(img)
	scipy.misc.imsave(output_filepath, img)

def is_wall(x, y, terrain_matrix):
	if x < 0 or x >= WIDTH:
		return False
	if y < 0 or y >= HEIGHT:
		return False
	ter = str(terrain_matrix[y][x])
	terrain_val_obj = TERRAIN_TEMPLATE_DICT.get(ter)
	if terrain_val_obj is None:
		return False
	return terrain_val_obj.get('tr_blockage_type1') == '3'
