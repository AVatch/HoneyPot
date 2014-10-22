import sys
import random

import prefix
import suffix
import l33t

'''
Main Functions
'''


def pollinateMe(p, k):
    # word_parts(p, 1)
    # l33t_word(p, 1)
    # delta_word(p, 1)


def unPollinateMe(p, k):
    pass

'''
Helper Functions
'''


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

# Execute Code
if __name__ == '__main__':
    args = sys.argv

    action = args[1]
    password = args[2]
    k_honey_words = args[3]
    training_data = args[4]

    if action == 'pollinate':
        print 'pollinating'
        pollinateMe(password, k_honey_words)
    elif action == 'unpollinate':
        print 'un-pollinating'
    else:
        print "unkown action"
