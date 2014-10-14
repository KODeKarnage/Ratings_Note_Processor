
# Standard modules
import os
import sys
import time


file_list = []

# Set the directory you want to start from
rootDir = 'V:\\Fund Research\\Private\\Qual Rating Reports'


def get_filenames():

	count = 0

	for dirName, subdirList, fileList in os.walk(rootDir):

		if dirName == rootDir:
			continue

		if not count % 100:
			print 'folder %s %s' % (count, dirName)

		# if count == 500:
		# 	break

		count += 1	


		for fname in fileList:

			fn = fname.lower()

			if all(['rating' in fn, 
					'.docx' in fn,
					'~' not in fn, 
					any(['note' in fn, 'template' in fn]),
				]):

				# file name
				f = os.path.join(dirName, fname)

				# file stats
				(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f)
				mod_time = time.ctime(mtime)

				file_list.append((f, mod_time))


	output_file = "C:\\Temp\\RN_filelist.txt"

	with open(output_file, 'w') as f:
		lines = [''.join([x[0], ' |::| ', str(x[1]), '\n']) for x in file_list]
		f.writelines(lines)

get_filenames()