''' A script to test scraping data from ratings notes stored on the file server '''

''' 
The script will traverse the folders on the file server and create a list of
tuples with the filename and date modified for any files with 'rating' and
'note' in the title. 

It then processes each file and extracts the desired data from the text.

'''

# Standard modules
import os
import sys
import pickle
import re
import random
import time

# Custom modules
import RN_toolbag as t
import ticker_secid as tsid
secid = tsid.tick_secid
# import folder_walker as fw

# desired output
des_out = {'SecID or Ticker': {
			'Date_presented': 'DATE_STRING',
            'Fund_Name': 'proper string',
            'Analysts': ['abc','def'],
            'Ratings': {
		            'Old': 'lowercase_string',
		            'Sug': 'lowercase_string',
		            'New': 'lowercase_string' },
			'Total': {
					'score': 0, 'out_of': 0, 'old': 0 },
			'People': {
					'score': 0, 'out_of': 0, 'old': 0 },
			'Process': {
					'score': 0, 'out_of': 0, 'old': 0 },
			'Parent': {
					'score': 0, 'out_of': 0, 'old': 0 },
			'Performance': {
					'score': 0, 'out_of': 0, 'old': 0 },
			'Price': {
					'score': 0, 'out_of': 0, 'old': 0 },
}}


def process_file(link):

	# test files
	test_file = "C:\\Temp\\Ratings_Note_Test_File.docx"
	# test_file = 'V:\\Fund Research\\Private\\Qual Rating Reports\\22_Asia & Emerging Markets\\2014\Ratings Committee\\Aberdeen Asian Opps (Ratings Note 2014).docx'
	pickle_file = "C:\\Temp\\RN_Pickle.txt"


	lines = t.get_docx_text(link)

	for line in lines:

		print line

	return lines[:25]


def get_name(lines):
	'''get Fund_Name '''

	# look within the first 2 lines for the name
	name_zone = lines[:2]

	for line in name_zone:

		#strip trailing whitespace from line
		line = line.strip()

		#check if there is a colon in the line
		if not all([':' in line.lower(), 
			any(['fund' in line.lower(),
				'strategy' in line.lower()])
				]):

			return line 

		elif all([':' in line.lower(), 
			any(['fund' in line.lower(),
				'strategy' in line.lower()])
				]):
			ix = line.index(':')

			line = line[ix+1:].lstrip()

			if line:

				return line

		else:

			return line


def get_ticker(lines):
	''' Get the ticker or the secID of the fund.
		It considers only the first 25 lines. '''	


	for i, v in enumerate(lines):

		if 'ticker' in v.lower():

			# find an instance of the word 'ticker' can slice the list after that
			name_zone = lines[i:]

			for line in name_zone:

				#strip trailing whitespace from line
				line = line.strip()

				#check if there is a colon in the line
				# if not, then return that line
				# check for a comma too, and take the first entry if there are multiple
				if not all([':' in line.lower(), 'ticker' in line.lower()]):

					possible_ticker = re.split('; |, | |,|\*|\n', line.lower())

					return possible_ticker[0]

				elif all([':' in line.lower(), 'ticker' in line.lower()]):

					ix = line.index(':')

					line = line[ix+1:].lstrip()

					possible_ticker = re.split('; |, | |,|\*|\n', line.lower())

					if possible_ticker:

						return possible_ticker[0]

				else:

					return possible_ticker


def get_ratings(lines):
	''' Get the various Ratings from the Note '''

	lines = lines[:50]
	Rating_Dict = {}
	grab = False

	for line in lines:

		if 'rating recommended' in line.lower():
			grab = 'New'
			continue

		elif 'rating suggested' in line.lower():
			grab = 'Sug'
			continue

		elif 'previous rating' in line.lower():
			grab = 'Old'
			continue

		if grab:
			Rating_Dict[grab] = line.strip().lstrip().lower()
			grab = False

	return Rating_Dict


def get_scores(lines):

	Score_Dict = {}

	scores = ['Total Scores', 'People', 'Process', 'Parent', 'Performance', 'Price']

	for score in scores:

		found = False

		for i, text in enumerate(lines):

			if found:
				break

			text = text.strip().lstrip().lower()

			# cycle through the lines to where the SCORE is found

			if text == score.lower():

				# create a new list of the 10 following lines

				new_score_space = lines[i+1:i+11]

				# cycle through those 10 lines

				for x, lyne in enumerate(new_score_space):

					# # escape the loop if x is the last line

					# if x == len(new_score_space)-1:
					# 	continue

					# 

					new_score_line = lyne.strip().lstrip()
					# print new_score_line

					# if the line has these items, then ignore them
					escape_chars = list('><()') + ['ilver', 'old', 'ronze','eutral','egative']
					req_chars = list('0123456789')

					
					if any(char in new_score_line for char in escape_chars):
						continue

					if not any(char in new_score_line for char in req_chars):
						continue

					else:

						if '/' in new_score_line:

							new_score_fraction = new_score_line.split('/')

							if len(new_score_fraction) > 1:

								ns = new_score_fraction[0]
								out_of = new_score_fraction[1]
							
							else:
								ns = new_score_fraction[0]
								out_of = 0

						else:
							ns = new_score_line
							out_of = 0

						try:
							old_score_line = new_score_space[x+1].strip().lstrip()

							if '/' in old_score_line:
								old_score_fraction = old_score_line.split('/')
								os = old_score_fraction[0]


							else:
								os = old_score_line
						except:
							os = 0

						if len(str(os)) > 2:
							os = os[:2].strip()

						Score_Dict[score] = {}
						Score_Dict[score]['score'] = ns
						Score_Dict[score]['out_of'] = out_of
						Score_Dict[score]['old'] = os

						found = True

						break


						# sys.exit()

	return Score_Dict


def get_analyst(lines):
	''' Gets the analyst names '''

	lines = lines[:20]

	grab = False

	for line in lines:
		if all([':' in line.lower(), 'analyst' in line.lower() ]):

			aline = line[line.index(':') + 1: ].strip().lstrip().lower()

			if aline:
				aline = aline.replace('.', '|')
				aline = aline.replace(',', '|')
				aline = aline.replace('&', '|')
				aline = aline.replace('/', '|')	
				aline = aline.replace('\\', '|')
				aline = aline.replace(' and ', '|')

				clean_analyst = [x.strip().lstrip() for x in aline.split("|")]

				return clean_analyst

			else:
				grab = True

		elif grab:

			if line:
				line = line.replace(',', '|')
				line = line.replace('.', '|')
				line = line.replace('&', '|')
				line = line.replace('/', '|')	
				line = line.replace('\\', '|')
				line = line.replace(' and ', '|')

				clean_analyst = [x.strip().lstrip() for x in line.split("|")]

				return clean_analyst

	return []


# a = r'V:\Fund Research\Private\Qual Rating Reports\Colonial First State\2013\Multisector\CFS GAM Multisector - Ratings Note.docx'.replace('\\','\\')
# # a = r'C:\Temp\Ratings_Note_Test_File2.docx'.replace('\\','\\')
# l = process_file(a)
# print get_scores(l)
# sys.exit()

analyst_list = []
count = 1

with open('C:\\Temp\\RN_filelist.txt', 'r') as f:

	scores = ['Total Scores', 'People', 'Process', 'Parent', 'Performance', 'Price']

	files = f.readlines()
	random.shuffle(files)


	# files = files[:100]

	for f in files:

		an_tup = ()
	
		print str(count) + ' / ' + str(len(files))
		count += 1

		if 'parent' in f.lower():
			continue

		link = f.split(' |::| ')


		lines = t.get_docx_text(link[0])


		# print "\n"
		# print "========"
		# print f
		date_str = link[1].replace('\n','')

		time_ob = time.strptime(date_str, '%a %b %d %H:%M:%S %Y')

		date = time.strftime('%d/%m/%Y', time_ob)

		# print "Name: %s" % get_name(lines)

		tick = get_ticker(lines)
		try:
			tick = int(tick)
			tick = secid.get(tick, "Not Found")
		except:
			pass

		# print "Ticker: %s" % tick
		# print 'Ratings: %s' % get_ratings(lines)
		# print 'Scores: %s' % get_scores(lines)
		# print 'Analyst: %s' % get_analyst(lines)
		# print 'Date: %s' % date

		an_tup = ()

		an_tup += (date,)
		an_tup += (tick,)
		an_tup += (get_name(lines).replace(',',' '),)

		raw_anal = [x for x in get_analyst(lines) if x]

		analyst_str = '+'.join(raw_anal)
		an_tup += (analyst_str,)

		rat_dict = get_ratings(lines)
		an_tup += (rat_dict.get('Old', ''), rat_dict.get('Sug', ''), rat_dict.get('New', ''))

		score_dict = get_scores(lines)
		for group in scores:
			an_tup += ( score_dict.get(group, {}).get('score', ''), 
						score_dict.get(group, {}).get('out_of', ''), 
						score_dict.get(group, {}).get('old', ''))

		an_tup += (f,)

		analyst_list.append(an_tup)
		# print f
		# print str(an_tup)

'''
(date, ticker, name, analyst, old, sug, new, tot, totoo, totold, ..., filename)
'''

with open('C:\\Temp\\Analysts.txt', 'w') as f:

	for a in analyst_list:

		f.write(str(a) + '\n')


# get ticker or SecID

# get ratings

# get scores
