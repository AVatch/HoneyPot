import sys
import random
import honey_functions as hf
from rock_you_generator import distance_ratio


'''
Main Functions
'''


def pollinateMe(p, k):
    pot = [p]

    # Get number of buckets
    buckets = random.randrange(1, k)
    while (k % buckets):
        buckets = random.randrange(1, k)
    count = int(k/buckets)

    # Choose a random seed for every bucket
    for i in range(0, buckets):
        # seed = random.choice(pot)
        seed = p
        # n_trans = random.randrange(1, len(hf.FUNCTIONS))
        n_trans = random.randrange(1, 3)
        # Choose a random function for every count in bucket
        for j in range(0, count):
            honey = seed
            # Transform word a random number of times
            for k in range(0, n_trans):
                weight = random.random()
                func = random.choice(hf.FUNCTIONS)
                honey = func(honey, weight)
                # Make sure the honey isn't already in the pot
                while honey in pot or distance_ratio(honey, p) <= 75:
                    func = random.choice(hf.FUNCTIONS)
                    honey = func(seed, weight)

                print func, '\t->\t', honey, '\t', distance_ratio(honey, p)
            pot.append(honey)

    random.shuffle(pot)
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
    if len(args) == 5:
        training_data = args[4]

    if action == 'pollinate':
        #print 'pollinating'
        words = pollinateMe(password, k_honey_words)
        print "*"*50
        print 'HONEY WORDS:\n', '\n'.join(words)
    elif action == 'unpollinate':
        print 'un-pollinating'
    else:
        print 'unknown action'
