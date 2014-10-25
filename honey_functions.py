import random

import prefix
import suffix

'''
Gives back a word with parts of it changed

'''
def word_parts(word, weight):
    #print "[Word Parts] Input:\t", word
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

    #print "[Word Parts] Output:\t", word
    return word

'''
Gives back a leet version of the given word

'''

L33T_LIST = [
    {'e': '3'},
    {'o': '0'},
    {'l', '1'},
    {'a', '@'}
]

def l33t_word(word, weight):
    #print "[l33t] Input:\t", word
    for char in word:
        p = random.random()
        if p <= weight:
            for i, j in enumerate(L33T_LIST):
                pass #print i, j
    #print "[l33t] Output:\t", word
    return word


'''
Gives back a word

'''
def delta_word(word, weight):
    #print "[delta word] Input:\t", word
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

    #print "[delta word] Output:\t", word
    return word


'''
Add all function names here
'''

FUNCTIONS = [
    word_parts,
    l33t_word,
    delta_word
]

