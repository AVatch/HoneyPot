import csv
from difflib import SequenceMatcher

'''
Reading in rock you data set, and cleaning it out, saves to new listanf file

'''

def clean_rock_passwords(filecsv):
	rock_passwords = []
	f = open(filecsv, 'rw')
	try:
	    reader = csv.reader(f)
	    for row in reader:
	    	temp = row[0].split()
	    	if len(temp) == 2:
	    		rock_passwords.append(temp[1])
	finally:
	    f.close()

	print "Done generating list of rock you passwords"
	print "Saving file to new list"

	rock_you_clean = open('rockyou_clean.csv', 'wb')
	writer = csv.writer(rock_you_clean, dialect = 'excel')
	for i in rock_passwords:
		writer.writerow([i])

def distace_ratio(s1, s2):
    if s1 is None:
        raise TypeError("s1 is None")
    if s2 is None:
        raise TypeError("s2 is None")
    if len(s1) == 0 or len(s2) == 0:
        return 0

    m = SequenceMatcher(None, s1, s2)
    print int((100 * m.ratio()))

distace_ratio("NEW YORK METS", "NEW YORK MEATS")
