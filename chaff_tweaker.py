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

def tail_tweaker(password):
	# tweaks the tail a substring of consecutives digits within 
	# a password with a random digit at end of string
	tuples = re.findall(r'(\w+?)(\d+)', password)
	for x,y in tuples[-1:]:
		tail = int(y) + random.randint(0,10)
		if password.replace(y,str(tail)) == password:
			password = password.replace(y,str(tail-1))
		else:
			password = password.replace(y,str(tail))
	print password

def head_tweaker(password):
	# tweaks the head of a password with random digits
	# if password doesn't start with digits returns same password
	tuples = re.findall(r'(\w+?)(\d+)', password)
	if tuples == []:
		print password 
	else:
		for y in tuples[0]:
			try:
				head = int(y) + random.randint(0,10)
				password = password.replace(y,str(head))
			except ValueError:
				break
		print password

def lower_case(password):
	# tweaks upper case letters to lower case
	new_password = ''
	for l in range(len(password)):
		if password[l].isupper() == True:
			new_password += password[l].lower()
		else:
			new_password += password[l]
	print new_password

def upper_case(password):
	# tweaks lower case letters to upper case in alternate fashion
	new_password = ''
	for l in range(0,len(password),2):
		if password[l].islower() == True:
			password = password.replace(password[l], password[l].upper())
		else:
			continue
	print password

## tests ##
year_tweaker('1234password19992010')
tail_tweaker('1234hihi55667934')
head_tweaker('1234hihi55667934')
head_tweaker('hihi55667934')
lower_case('Password1234Hello')
tail_tweaker('1234pass345word567')
upper_case('forever')
head_tweaker('pass5555word')


