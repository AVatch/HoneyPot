import numpy as np
import csv
import datetime
import random
import enchant
from rock_you_generator import distance_ratio


def loadtxt(f):
    password = np.loadtxt(f,
                          delimiter='\n',
                          dtype={
                                 'names': ('password',),
                                 'formats': ('S99',)},
                          unpack=True)
    return password


def check_against_rockyou(p, rockyou):
    for w in rockyou:
        if w == p:
            return True
    return False

'''
Helper Functions
'''

def entropy_score(word):
    upper = 0.
    lower = 0.
    digits = 0.
    special = 0.
    for i in word:
        if i.isdigit():
            digits += 1
        elif i.isupper():
            upper += 1
        elif i.islower():
            lower += 0
        else:
            special += 1
    score = int(round(1 - (upper + lower + digits + special)/len(word)))

    return score

def root_score(word, wordlist):
    score = 0
    for i in range(len(wordlist)):
        if word in wordlist[i][0]:
            score += 1
    return score

def spelling_score(word):
    d = enchant.Dict("en_US")
    word = word.lower()
    word = word.translate(None, '!@#$%^&*_-=+~1234567890')
    if d.check(word):
        return 1
    else:
        return 0

def similarity_score(word, wordlist):
    pass

def get_score(word, wordlist):
    e_score = entropy_score(word)
    r_score = root_score(word, wordlist)
    s_score = spelling_score(word)

    total = e_score + r_score + s_score
    return total

# Load data
filename = "group1"
filename = "foreign_honey/honeywords"
password_number = random.randint(1,300)
pass_file = loadtxt(filename+"/"+str(password_number))
#print "[", datetime.datetime.now(), "]\tlodaed password"
rockyou = []
rockyou_threshold = 10
with open("rockyou_clean.csv", "r") as rf:
    reader = csv.reader(rf)
    for row in reader:
        if len(rockyou) > rockyou_threshold - 1:
            break
        else:
            rockyou.append(row[0])
#print "[", datetime.datetime.now(), "]\tlodaed rockyou"
#print rockyou

# Create similiarity matrix
pass_matrix = [[] for x in range(0, len(pass_file))]

for i in range(len(pass_file)):
    for j in range(len(pass_file)):
        dist = distance_ratio(pass_file[i][0], pass_file[j][0])
        pass_matrix[i].append(dist)

print "*"*50
print '\t00, 01, 02, 03, 04, 05, 06, 07, 08, 09'
for i in range(len(pass_matrix)):
    print i, '\t', pass_matrix[i]

# Pull out pairs of similiar entries
threshold = 80
pairs = []
for i in range(len(pass_matrix)):
    for j in range(len(pass_matrix[i])):
        if pass_matrix[i][j] >= threshold and pass_matrix[i][j] != 100:
            p1 = pass_file[i][0]
            p2 = pass_file[j][0]
            pollen = [p1, p2, pass_matrix[i][j]]
            redundant_pollen = [p2, p1, pass_matrix[i][j]]
            if pollen not in pairs and redundant_pollen not in pairs:
                pairs.append(pollen)

print "*"*50
print "Above threshold: ", threshold
for i in pairs:
    print i

# Create a set of honey words
print "*"*50
honey_words_to_break = []
for i in range(len(pairs)):
    if len(honey_words_to_break) == 0:
        honey_words_to_break.append(pairs[i][0])
    if pairs[i][0] not in honey_words_to_break:
        honey_words_to_break.append(pairs[i][0])

# If it's a known set, then print the actual password (FOR TESTING)
if filename == "group1":
    with open("group1.txt") as f:
        lines = f.readlines()    
        print "Original Password: " + lines[password_number-1]

print "List of all honeywords in file"
for i in range(len(pass_file)):
    p = pass_file[i][0]
    score = get_score(p,pass_file)
    print p + " : " + str(score)
# print pass_file
print "List of honey words above threshold"
print honey_words_to_break

print "Password Number: " + str(password_number)
