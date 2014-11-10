import sys
import random
import honey_functions as hf
import os
import math
from rock_you_generator import distance_ratio, rock_you_like_a_hurricane


'''
Main Functions
'''
def pollinate(p, k, data_size):
    passwords = rock_you_like_a_hurricane(p, k, data_size)
    #passwords.append(p)
    rseeds = [] # Seeds originating from rock you
    pseeds = [] # Seeds originating from p

    # Add more seeds
    pseeds.append(p)
    
    while len(pseeds) < 2:
        for func in hf.FUNCTIONS[0:6]:
            pw = func(p,1)
            if not pw in pseeds:
                pseeds.append(pw)
                break

    for pw in passwords:
        rseeds.append(pw)

    while len(rseeds) < 2*len(passwords):
        for func in hf.FUNCTIONS[0:6]:
            pw = random.choice(rseeds)
            pw2 = func(pw,1)
            if not pw2 in rseeds:
                rseeds.append(pw2)
                break

    seeds = pseeds + rseeds
    #print seeds
    pot = [p]

    # Get number of buckets
    max_buckets = max(int(math.ceil(k/3)),3)
    buckets = random.randrange(2,max_buckets)
    count = int(math.ceil(k/buckets))

    # Choose random seed and add honeywords for each bucket
    last_length = len(pot)
    seed = pseeds[1]
    while len(pot) < k + 1:
        if len(pot) == last_length + count:
            seed = random.choice(seeds)
            last_length = len(pot)
        pot = pollinate_me(seed,pot)

    random.shuffle(pot)
    return pot


def pollinate_me(p, pot):
    max_trans = 1 
    n_trans = random.randrange(1,3)
    honey = p
    threshhold = 75
    
    for k in range(0, n_trans):
        weight = random.random()
        func = random.choice(hf.FUNCTIONS)
        honey = func(honey, weight)
            # print func, '\t->\t', honey, '\t', distance_ratio(honey, p)

    if not (honey in pot) and (distance_ratio(honey, p) > threshhold):
        pot.append(honey)

    return pot


def unpollinate_me(p, k):
    pass

def pollinate_file(p, k):
    d_size = None
    directory, ext = os.path.splitext(p)
    directory = directory
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(p) as f_in:
        for i, line in enumerate(f_in):
            print i + 1, line.strip()
            if i < 100:
                d_size = 0
            elif i < 200:
                d_size = 100
            else:
                d_size = 3000000
            words = pollinate(line.strip(), k_honey_words, d_size)
            f_out_name = directory + "/" + str(i + 1)
            with open(f_out_name,'w+') as f_out:
                f_out.write('\n'.join(words))

    

'''
Helper Functions
'''


def entropy(word):
    upper = 0
    lower = 0
    digits = 0
    for i in word:
        if i.isdigit():
            digits += 1
        if i.isupper():
            upper += 1
        if i.islower():
            lower += 1

    print upper, '\t', lower, '\t', digits


# Execute Code
if __name__ == '__main__':
    args = sys.argv

    action = args[1]
    password = args[2]
    k_honey_words = int(args[3])
    d_size = None
    if len(args) > 4:
        d_size = int(args[4])

    if action == 'pollinate':
        words = pollinate(password, k_honey_words, d_size)
        print "*"*50
        print 'HONEY WORDS:\n', '\n'.join(words)
    elif action == 'pollinate_file':
        pollinate_file(password, k_honey_words)
    elif action == 'unpollinate':
        print 'un-pollinating'
    else:
        print 'unknown action'
