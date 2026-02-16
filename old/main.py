import csvFormatter
import parsers.zoneParser as zoneParser
import os
import zone_data_to_csv_parser as zone_csv_parser
import gf_exe_to_csv_parser as gf_exe_parser
import imageSplitter

import zoneImager

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5/Geneforge 5 Files')
GENEFORGE_DATA_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'aGF5ScenData.dat')

ZONE_IMAGE_OUTPUT_FILE = 'geneforge5/static/geneforge5/images/'
ITEM_IMAGE_OUTPUT_FILE = 'geneforge5/static/geneforge5/images/items/'

def main():
	#imageSplitter.splitItemImages(ITEM_IMAGE_OUTPUT_FILE)

	#csvFormatter.parseAllToCsv()
	zone_csv_parser.parse_zones()
	#gf_exe_parser.parse_exe()
	return

	for zone in range(82):
		zone_dict = zoneParser.parsezone(GENEFORGE_DATA_FILE_PATH, zone)
		#zoneParser.outputprint(zone_dict)
		zoneImager.create_zone_image(zone_dict['terrain'], ZONE_IMAGE_OUTPUT_FILE + '{}.png'.format(zone))

if __name__ == '__main__':
	main()
