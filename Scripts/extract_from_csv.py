''' This script takes the results of an abstractive summarization script and uses Keybert 
to extract keywords from those summaries. Usage:

python extract_from_csv.py <input_csv_file>

'''

import sys
import os
from keybert import KeyBERT
import csv


#_________________________________________________
# MAIN
#_________________________________________________

	
filepath = "TEXT EXTRACTION FROM XML.xlsx - Sheet1.csv"
outpath = "outfile.csv"


# Lecture du fichier d'entrée
file = open(filepath, "r")
listObj = list(csv.reader(file))

outfile = open(outpath, "w")
writer = csv.writer(outfile)

kw_model = KeyBERT()


writer.writerow(listObj[0])
listObj.pop(0)


for row in listObj:
	keywordlist = []
	keywordlist[0:1] = row[0:1]
	row.pop(0)
	
	for current_text in row:
		print(current_text)
		print("\n")
		

		keywords_MMR = kw_model.extract_keywords(current_text, keyphrase_ngram_range=(1, 2), stop_words='english',
								  use_mmr=True, diversity=0.6)

		keywords_MMR = [tup[0] for tup in keywords_MMR if tup[1] > .5]
		print(keywords_MMR)
		
		

		keywords_MSD = kw_model.extract_keywords(current_text, keyphrase_ngram_range=(1, 3), stop_words='english',
								  use_maxsum=True, nr_candidates=30, top_n=5)
		keywords_MSD = [tup[0] for tup in keywords_MSD if tup[1] > .5]
		print(keywords_MSD)
		

		keystring = ", ".join(keywords_MSD)
		
		if len(keywords_MMR) > 0 and len(keywords_MSD) > 0:
			keystring += ", "

		keystring += ",".join(keywords_MMR)

		
		
		print(keystring)
		
		keywordlist.append(keystring)

	writer.writerow(keywordlist)


outfile.close()
