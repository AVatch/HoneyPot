## Tail or Head tweaker

import datetime
import re
import random

def year_tweaker(password):
	## detects yr between 1950-2014 and changes yr
	## to year + 1 in password
	match = re.findall(r'\d{4}', password)
	for m in match:
		if int(m) in range(1950,2015):
			n = int(m) + 1
			password = password.replace(m,str(n))
	print password

def tail_teaker(password):
	#tweaks the tail of a password with a random digit at the end
	tuples = re.findall(r'(\w+?)(\d+)', password)
	for x,y in tuples[-1:]:
		tail = int(y) + random.randint(0,10)
		password = password.replace(y,str(tail))
	print password

def head_tweaker(password):
	#tweaks the head of a password with random digits
	tuples = re.findall(r'(\w+?)(\d+)', password) 
	for y in tuples[0]:
		head = int(y) + random.randint(0,10)
		password = password.replace(y,str(head))
	print password

## test ##
year_tweaker('1234password19992010')
tail_teaker('1234hihi55667934')
head_tweaker('1234hihi55667934')