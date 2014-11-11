import numpy as np
import csv
import datetime
import random
import enchant
import re
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

def word_score(word):
    d = enchant.Dict("en_US")
    word = word.lower()
    word = word.translate(None, '!@#$%^&*_-=+~1234567890')
    if not word == '':
        if d.check(word):
            return 1
    return 0

def rockyou_score(word, rockyou, password_number):
    if password_number < 100: 
        for w in rockyou:
            if w == word:
                return 1
    return 0

def year_score(word):
    match = re.findall(r'\d{4}', word)
    for m in match:
        if int(m) in range(1950, 2015):
            return 1
        else:
            return 0
    return 0
 

def similarity_set(wordlist, debug):
    # Create similiarity matrix
    pass_matrix = [[] for x in range(0, len(wordlist))]

    for i in range(len(wordlist)):
        for j in range(len(wordlist)):
            dist = distance_ratio(wordlist[i][0], wordlist[j][0])
            pass_matrix[i].append(dist)

    if debug:
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
                p1 = wordlist[i][0]
                p2 = wordlist[j][0]
                pollen = [p1, p2, pass_matrix[i][j]]
                redundant_pollen = [p2, p1, pass_matrix[i][j]]
                if pollen not in pairs and redundant_pollen not in pairs:
                    pairs.append(pollen)

    if debug: 
        print "*"*50

    honey_words_to_break = []
    for i in range(len(pairs)):
        if len(honey_words_to_break) == 0:
            honey_words_to_break.append(pairs[i][0])
        if pairs[i][0] not in honey_words_to_break:
            honey_words_to_break.append(pairs[i][0])
    
    if debug:
        print "List of honey words above threshold"
        print honey_words_to_break

    return honey_words_to_break


def guess_password(wordlist, rockyou, password_number, debug = False):
    word_scores = [] #[[] for x in range(0, len(wordlist))]
    s_set = similarity_set(wordlist, debug)

    for i in range(len(wordlist)):
        total = 0
        word = wordlist[i][0]
        e_score = entropy_score(word)
        r_score = root_score(word, wordlist)
        w_score = word_score(word)
        y_score = year_score(word)
        ry_score = rockyou_score(word, rockyou, password_number)
        total = e_score + r_score + w_score + y_score + ry_score
        if word in s_set:
            total += 1
        word_scores.append([word, total])

    if debug: print word_scores

    if debug:
        print "*"*50
        print "List of all honeywords in file"
        for s in word_scores:
            print s

    # Figure out the maximum score
    max_score = 0
    chosen_word = ''
    for ind, s in enumerate(word_scores):
        if word_scores[ind][1] > max_score:
            max_score = word_scores[ind][1]
            chosen_word = word_scores[ind][0]

    return chosen_word

# Execute Code
if __name__ == '__main__':
    # Load data
    filename = "group1"
    #filename = "foreign_honey/honeywords"

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

    debug = False
    password_guess_list = []

    if debug:
        password_number = random.randint(1,300)
        print "Password Number: " + str(password_number)
        pass_file = loadtxt(filename+"/"+str(password_number))
        # If it's a known set, then print the actual password (FOR TESTING)
        if filename == "group1":
            with open("group1.txt") as f:
                lines = f.readlines()    
                print "Original Password: " + lines[password_number-1]

        chosen_word = guess_password(pass_file, rockyou, password_number, debug)

    else:
        correct_count = 0.
        for i in range(1,300):
            password_number = i
            pass_file = loadtxt(filename+"/"+str(password_number))
            chosen_word = guess_password(pass_file, rockyou, password_number, debug)
            password_guess_list.append(chosen_word)

            # If it's a known set, then print the actual password (FOR TESTING)
            if filename == "group1":
                with open("group1.txt") as f:
                    lines = f.readlines()    
                    original_word = lines[password_number-1].strip() 
                    print "Original Password: " + original_word + " \t\t\t Chosen Password: " + chosen_word
                    if original_word == chosen_word:
                        correct_count += 1
        print "Percentage Correct: " + str(correct_count/300.)

