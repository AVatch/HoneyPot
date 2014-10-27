import random
import re
import prefix
import suffix

'''
IMPORTANT: Add all function names to list 'FUNCTIONS' at
the bottom of this file.
'''


def word_parts(word, weight):
    #print "[Word Parts] Input:\t", word
    p = random.random()
    if p <= weight:
        # Switch both pre + suff
        for i in prefix.PREFIX_LIST:
            if i in word[:len(word)-len(word)/3] or i in word[len(word)-len(word)/3:]:
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

L33T_LIST = {
    'a': '@', 'b': '13', 'e': '3', 'f': 'ph', 'g': '6',
    'o': '0', 'l': '1', 's': '$', 'r': 'i2', 'w': 'vv'
}


def l33t_word(word, weight):
    #print "[l33t] Input:\t", word
    word = list(word)
    for i, char in enumerate(word):
        p = random.random()
        if p < weight:
            if char in L33T_LIST:
                word[i] = L33T_LIST[char]
    word = "".join(word)
    #print "[l33t] Output:\t", word
    return word


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
                    word[ind] = str(abs(int(char) - 1))
                    word = "".join(word)

    #print "[delta word] Output:\t", word
    return word


def year_tweaker(password, weight=1):
    ## detects yr between 1950-2014 and changes yr
    ## to year + 1 in password
    match = re.findall(r'\d{4}', password)
    for m in match:
        if int(m) in range(1950, 2015):
            n = int(m) + 1
            password = password.replace(m, str(n))
    return password


def tail_tweaker(password, weight=1):
    # tweaks the tail a substring of consecutives digits within
    # a password with a random digit at end of string
    tuples = re.findall(r'(\w+?)(\d+)', password)
    for x, y in tuples[-1:]:
        tail = int(y) + random.randint(0, 10)
        if password.replace(y, str(tail)) == password:
            password = password.replace(y, str(tail-1))
        else:
            password = password.replace(y, str(tail))
    return password


def head_tweaker(password, weight=1):
    # tweaks the head of a password with random digits
    # if password doesn't start with digits returns same password
    tuples = re.findall(r'(\w+?)(\d+)', password)
    if tuples == []:
        return password
    else:
        for y in tuples[0]:
            try:
                head = int(y) + random.randint(0, 10)
                password = password.replace(y, str(head))
            except ValueError:
                break
        return password


def lower_case(password, weight=1):
    # tweaks upper case letters to lower case
    new_password = ''
    for l in range(len(password)):
        if password[l].isupper() is True:
            new_password += password[l].lower()
        else:
            new_password += password[l]
    return new_password


def upper_case(password, weight=1):
    # tweaks lower case letters to upper case in alternate fashion
    for l in range(0, len(password), 2):
        if password[l].islower() is True:
            password = password.replace(password[l], password[l].upper())
        else:
            continue
    return password


'''
Add all function names here
'''

FUNCTIONS = [
    # word_parts,
    l33t_word,
    delta_word,
    year_tweaker,
    tail_tweaker,
    head_tweaker,
    lower_case,
    upper_case,
]
