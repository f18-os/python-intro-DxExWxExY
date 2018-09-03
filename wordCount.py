import sys
import re
import os
import collections

# global variables
input_file = ""
output_file = ""

# method used for reeading a file
def check_arguments():
	if len(sys.argv) is not 3:
		print("Arguments Mismatch, Try Again.")
		exit()
	else:
		global input_file
		global output_file
		input_file = sys.argv[1]
		output_file = sys.argv[2]
		if not os.path.exists(input_file):
			print("Input File not Found.")
			exit()
		else:
			purge_file()

# purges the punctuation and \n from the file
def purge_file():
	reader = open(input_file, 'r')
	data = reader.read()
	purged_data = re.sub('\W+', ' ', data)
	purged_data = re.sub('\s+', ' ', purged_data)
	words = purged_data.split(' ')
	reader.close()
	build_dictionary(words)

# builds the dictionary for mapping
def build_dictionary(words):
	dictionary = {}
	for word in words:
		if word.lower() in dictionary:
			dictionary[word.lower()] += 1
		else:
			dictionary[word.lower()] = 1
	sorted_dictionary = collections.OrderedDict(sorted(dictionary.items()))
	if '' in sorted_dictionary:
		sorted_dictionary.pop('', None)
	writer = open(output_file, 'w+')
	for w, c in sorted_dictionary.items():
		writer.write("%s %s\n" %(w, c))

# psychological main
check_arguments()