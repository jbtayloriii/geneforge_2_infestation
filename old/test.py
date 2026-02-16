
import re
import os

GENEFORGE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5')

GENEFORGE_EXE = os.path.join(GENEFORGE_DIR, 'Geneforge 5.exe')

GENEFORGE_DAT_FILE = os.path.join(GENEFORGE_DIR, 'Geneforge 5 Files/aGF5ScenData.dat')

''' Test script to find hex values in files '''

def main():
	with open(GENEFORGE_DAT_FILE, mode='rb') as f:
			#80, 85, 90
		l1 = []
		l2 = []
		l3 = []

		place = 0

		bytes = f.read(2)
		while bytes != b'':
			if place == 32:
				print(bytes)

			place = place + 1
			if bytes == b'\x50\x00':
				l1.append(place)
			if bytes == b'\x55\x00':
				l2.append(place)
			if bytes == b'\x5a\x00':
				l3.append(place)
			bytes = f.read(2)


		print(l1)
		print(l2)
		print(l3)

		for x in l1:
			if is_close(x, l2) and is_close(x, l3):
				print(x)

def is_close(x, num_list):
	min = 0
	max = len(num_list)
	while(min < max):
		pos = (min + max) // 2
		val = num_list[pos]
		if abs(val - x) < 100:
			return True
		elif val < x:
			min = pos + 1
		else:
			max = pos - 1

	return False

if __name__ == '__main__':
	main()
