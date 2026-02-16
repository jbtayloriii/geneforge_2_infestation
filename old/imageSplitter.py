from scipy import misc
import numpy as np
import os

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5/Geneforge 5 Files')

ITEM_IMAGE_FILES = [os.path.join(GENEFORGE_FILE_DIR, 'Graphics A/G1500.bmp'), os.path.join(GENEFORGE_FILE_DIR, 'Graphics A/G1510.bmp')]
ITEM_IMAGE_DIMENSIONS = (32, 32)
ITEM_IMAGE_ROWS = 10
ITEM_IMAGE_COLS = 20


def splitItemImages(outputDir):
	for filename in ITEM_IMAGE_FILES:
		f = misc.imread(filename)
		for row in range(ITEM_IMAGE_ROWS):
			for col in range(ITEM_IMAGE_COLS):
				itemfilename = 'item_{}_{}_{}.png'.format('50' if filename == ITEM_IMAGE_FILES[0] else '51', row, col)
				print(itemfilename)
