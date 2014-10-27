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
    buckets = random.randrange(1,k)
    while (k % buckets):
        buckets = random.randrange(1,k)
    count = int(k/buckets)

    # Choose a random seed for every bucket
    for i in range(0,buckets) :
        seed = random.choice(pot)
        n_trans = random.randrange(1,len(hf.FUNCTIONS))
        # Choose a random function for every count in bucket
        for j in range(0,count) :
            honey = seed
            # Transform word a random number of times
            for k in range(0,n_trans) :
                weight = random.random()
                func = random.choice(hf.FUNCTIONS)
                honey = func(honey,weight)
                # Make sure the honey isn't already in the pot
                while honey in pot:
                    func = random.choice(hf.FUNCTIONS)
                    honey = func(honey,weight)
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


def word_parts(word, weight):
    print "[Word Parts] Input:\t", word
    p = random.random()
    if p <= weight:
        # Switch both pre + suff
        for i in prefix.PREFIX_LIST:
            if i in word:
                r = int(random.random()*len(prefix.PREFIX_LIST))
                word = word.replace(i, prefix.PREFIX_LIST[r])
                break

        for j in suffix.SUFFIX_LIST:
            if j in word:
                r = int(random.random()*len(suffix.SUFFIX_LIST))
                word = word.replace(j, suffix.SUFFIX_LIST[r])
                break
    else:
        # Switch only one
        r = random.random()
        if r <= 0.5:
            # Replace only the prefix
            for i in prefix.PREFIX_LIST:
                if i in word:
                    r = int(random.random()*len(prefix.PREFIX_LIST))
                    word = word.replace(i, prefix.PREFIX_LIST[r])
                    break
        else:
            # replace only the suffix
            for j in suffix.SUFFIX_LIST:
                if j in word:
                    r = int(random.random()*len(suffix.SUFFIX_LIST))
                    word = word.replace(j, suffix.SUFFIX_LIST[r])
                    break

    print "[Word Parts] Output:\t", word
    return word


def l33t_word(word, weight):
    print "[l33t] Input:\t", word
    p = random.random()
    for char in word:
        if p <= weight:
            for i, j in enumerate(l33t.L33T_LIST):
                print i, j
    print "[l33t] Output:\t", word


def delta_word(word, weight):
    print "[delta word] Input:\t", word
    p = random.random()
    for ind, char in enumerate(word):
        if char.isdigit():
            if p <= weight:
                r = random.random()
                if r <= 0.5:
                    word = list(word)
                    word[ind] = str(int(char) + 1)
                    word = "".join(word)
                else:
                    word = list(word)
                    word[ind] = str(int(char) - 1)
                    word = "".join(word)
    print "[delta word] Output:\t", word
    return word


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
        print ('HONEY WORDS:\n', '\n'.join(words))
    elif action == 'unpollinate':
        print ('un-pollinating')
    else:
        print ('unknown action')
