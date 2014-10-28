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
    print passwords
    pot = [p]
    # Get number of buckets
    buckets = int(math.ceil(k/2))
    seed = random.choice(passwords)
    pot = pollinateMe(seed,buckets,pot)
    pot = pollinateMe(p,k-buckets,pot)

    # # Choose a random seed for every bucket
    # for i in range(0, buckets):
    #     seed = random.choice(passwords)
    #     pot = pollinateMe(seed,count,pot)
    random.shuffle(pot)
    return pot




def pollinateMe(p, count, pot): 
    n_trans = random.randrange(1, 4)
    # Choose a random function for every count in bucket
    for j in range(0, count):
        honey = p
        threshhold = 75
        # Transform word a random number of times
        for k in range(0, n_trans):
            weight = random.random()
            func = random.choice(hf.FUNCTIONS)
            honey = func(honey, weight)
            # Make sure the honey isn't already in the pot
            whC = 0
            while honey in pot or distance_ratio(honey, p) <= threshhold:
                func = random.choice(hf.FUNCTIONS)
                honey = func(p, weight)
                whC += 1
                if whC == 100:
                    threshhold -= 5
                    p = random.choice(pot)
            print func, '\t->\t', honey, '\t', distance_ratio(honey, p)
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
