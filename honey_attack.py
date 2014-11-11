import numpy as np
import csv
import datetime
import random
import enchant
import re
import sklearn.linear_model as sk
from sklearn.svm import SVC
from rock_you_generator import distance_ratio


def loadtxt(f):
    password = np.loadtxt(f,
                          delimiter='\n',
                          comments=None,
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
    score = 1 - (upper + lower + digits + special)/len(word)

    return score

def root_score(word, wordlist):
    score = 0.
    for i in range(len(wordlist)):
        if word in wordlist[i][0]:
            score += 1
    return score/len(wordlist)

def word_score(word):
    d = enchant.Dict("en_US")
    word = word.lower()
    word = word.translate(None, '!@#$%^&*_-=+~1234567890')
    if not word == '':
        if d.check(word):
            return 1.
    return 0.

def rockyou_score(word, rockyou, password_number):
    if password_number < 100: 
        for w in rockyou:
            if w == word:
                return 1.
    return 0.

def year_score(word):
    match = re.findall(r'\d{4}', word)
    for m in match:
        if int(m) in range(1950, 2015):
            return 1.
    return 0.
 

def similarity_scores(wordlist, debug):
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

    # honey_words_to_break = []
    # for i in range(len(pairs)):
    #     if len(honey_words_to_break) == 0:
    #         honey_words_to_break.append(pairs[i][0])
    #     if pairs[i][0] not in honey_words_to_break:
    #         honey_words_to_break.append(pairs[i][0])

    honey_occurences = np.zeros(10)
    for i, w in enumerate(wordlist):
        for p in pairs:
            if p[0] == w[0]:
                honey_occurences[i] = 1
    #if len(pairs)>0: honey_occurences = honey_occurences/len(pairs)

    return honey_occurences


def train_guesser(p_file, hp_dir, rockyou, debug = False):
    predictor_x = np.zeros((3000,6))
    predictor_y = np.zeros(3000)
    real_words = []

    with open(p_file) as f:
        real_words = f.readlines()

    for i in range(0,300):
        password_number = i + 1
        wordlist = loadtxt(hp_dir+"/"+str(password_number))
        features = get_features(wordlist, rockyou, password_number, debug)

        for j in range(len(wordlist)):
            word = wordlist[j][0]
            predictor_x[10*i + j] = features[j,:]
            predictor_y[10*i + j] = 1. if word == real_words[i].strip() else 0.

    pr = sk.LinearRegression()
    #pr = SVC()
    pr.fit(predictor_x, predictor_y)
    return pr


def get_features(wordlist, rockyou, password_number, debug = False):
    s_scores = similarity_scores(wordlist,debug)
    feature_array = np.zeros((10,6))
    for i in range(len(wordlist)):
            word = wordlist[i][0]
            e_score = entropy_score(word)
            r_score = root_score(word, wordlist)
            w_score = word_score(word)
            y_score = year_score(word)
            ry_score = rockyou_score(word, rockyou, password_number)
            feature_array[i] = [e_score, r_score, w_score, y_score, ry_score, s_scores[i]]

    return feature_array


def guess_password(wordlist, rockyou, password_number, debug = False):
    word_scores = [] #[[] for x in range(0, len(wordlist))]
    features = get_features(wordlist, rockyou, password_number, debug)

    for i in range(len(wordlist)):
        total = 0
        word = wordlist[i][0]
        total = np.sum(features[i,:])
        word_scores.append([word, total])

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
    dir_name = "group1"
    #dir_name = "foreign_honey/honeywords"

    # Load Rockyou Dataset
    rockyou = []
    rockyou_threshold = 10000
    with open("rockyou_clean.csv", "r") as rf:
        reader = csv.reader(rf)
        for row in reader:
            if len(rockyou) > rockyou_threshold - 1:
                break
            else:
                rockyou.append(row[0])

    debug = False   ### Set to True to print a single file analysis, false to write to file our guesses

    min_pw = 1
    max_pw = 300
    if debug:
        min_pw = random.randint(1,300)
        max_pw = min_pw

    password_guess_list = []

    correct_count = 0.

    for i in range(min_pw,max_pw + 1):

        if debug: print "Password Number: " + str(max_pw)   

        password_number = i
        pass_file = loadtxt(dir_name+"/"+str(password_number))
        chosen_word = guess_password(pass_file, rockyou, password_number, debug)
        password_guess_list.append(chosen_word)
        file_name = dir_name + '.txt'

    group_file = open(file_name, 'wb')
    writer = csv.writer(group_file, dialect='excel')
    for p in password_guess_list:
        writer.writerow([p])


        # If it's a known set, then print the actual password (FOR TESTING)
        if dir_name == "group1":
            with open("group1.txt") as f:
                lines = f.readlines()    
                original_word = lines[password_number-1].strip() 
                if debug: print "Original Password: " + original_word + " \t\t Chosen Password: " + chosen_word
                if original_word == chosen_word:
                    correct_count += 1

    # TEST REGRESSION MODEL #

    cc_model = 0.
    model = train_guesser("group1.txt", dir_name, rockyou, debug)

    for i in range(min_pw,max_pw + 1):
        max_score = 0
        chosen_word = ''
        password_number = i
        pass_file = loadtxt(dir_name+"/"+str(password_number))
        features = get_features(pass_file, rockyou, password_number, debug)

        for j in range(len(pass_file)):
            word = pass_file[j][0]
            score = model.predict(features[j,:])
            if score > max_score:
                max_score = score
                chosen_word = word

        if dir_name == "group1":
            with open("group1.txt") as f:
                lines = f.readlines()    
                original_word = lines[password_number-1].strip() 
                print "Original Password: " + original_word + " \t\t Chosen Password: " + chosen_word
                if original_word == chosen_word:
                    cc_model += 1


    print "Percentage Correct: " + str(100*correct_count/300.) +"%"
    print "Percentage Correct (model): " + str(100*cc_model/300.) +"%"

    print len(password_guess_list)

