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

# Custom modules
import RN_toolbag as t
import folder_walker as fw

# desired output
des_out = {'SecID or Ticker': {
			'Date_presented': 'DATE_STRING',
            'Fund_Name': 'proper string',
            'Ratings': {
		            'Old': 'lowercase_string',
		            'Sug': 'lowercase_string',
		            'New': 'lowercase_string' },
			'Total': {
					'score': 0, 'out_of': 0 },
			'People': {
					'score': 0, 'out_of': 0 },
			'Process': {
					'score': 0, 'out_of': 0 },
			'Parent': {
					'score': 0, 'out_of': 0 },
			'Performance': {
					'score': 0, 'out_of': 0 },
			'Price': {
					'score': 0, 'out_of': 0 },
}}


# test files
test_file = "C:\\Temp\\Ratings_Note_Test_File.docx"
test_file = 'V:\\Fund Research\\Private\\Qual Rating Reports\\10_Multi Sector\\2013\Ratings Committee 1\\Workings\\2013 0130 Schroder Balanced (Ratings Note).docx'
pickle_file = "C:\\Temp\\RN_Pickle.txt"


lines = t.get_docx_text(test_file)[:25]

for line in lines:

	print line.encode('utf-8')
