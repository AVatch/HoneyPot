import sys
import random
import honey_functions as hf
import math
from rock_you_generator import distance_ratio, rock_you_like_a_hurricane


'''
Main Functions
'''
def pollinate(p, k, data_size):
    passwords = rock_you_like_a_hurricane(p, k, data_size)
    passwords.append(p)
    seeds = []
    print passwords

    # Add more seeds
    for pw in passwords:
        seeds.append(pw)
        for i in xrange(int(math.ceil(k/len(passwords)))):
            pw2 = hf.head_tweaker(hf.tail_tweaker(pw,1),1)
            if not pw2 in seeds:
                seeds.append(pw2)

    print seeds
    pot = [p]

    # Get number of buckets
    max_buckets = max(int(math.ceil(k/3)),3)
    buckets = random.randrange(2,max_buckets)
    count = int(math.ceil(k/buckets))

    # Choose random seed and add honeywords for each bucket
    last_length = len(pot)
    seed = p
    while len(pot) < k + 1:
        if len(pot) == last_length + count:
            seed = random.choice(seeds)
            last_length = len(pot)
        pot = pollinateMe(seed,pot)

    random.shuffle(pot)
    return pot


def pollinateMe(p, pot):
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


def unPollinateMe(p, k):
    pass


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
    d_size = int(args[4])

    if action == 'pollinate':
        words = pollinate(password, k_honey_words, d_size)
        print "*"*50
        print 'HONEY WORDS:\n', '\n'.join(words)
    elif action == 'unpollinate':
        print 'un-pollinating'
    else:
        print 'unknown action'
