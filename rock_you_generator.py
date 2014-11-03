import csv
from difflib import SequenceMatcher

'''
Reading in rock you data set, and cleaning it out, saves to new listanf file

'''


def clean_rock_passwords(filecsv):
    rock_passwords = []
    f = open(filecsv, 'rw')
    try:
        reader = csv.reader(f)
        for row in reader:
            temp = row[0].split()
            if len(temp) == 2:
                rock_passwords.append(temp[1])
    finally:
        f.close()

    print "Done generating list of rock you passwords"
    print "Saving file to new list"

    rock_you_clean = open('rockyou_clean.csv', 'wb')
    writer = csv.writer(rock_you_clean, dialect='excel')
    for i in rock_passwords:
        writer.writerow([i])


def distance_ratio(s1, s2):
    if s1 is None:
        raise TypeError("s1 is None")
    if s2 is None:
        raise TypeError("s2 is None")
    if len(s1) == 0 or len(s2) == 0:
        return 0

    m = SequenceMatcher(None, s1, s2)
    return int((100 * m.ratio()))


def rock_you_like_a_hurricane(p, n, d_size = None):
    hot_passes = []
    pass_dist = []
    with open('rockyou_clean.csv', 'r') as f:
        for i,row in enumerate(f):
            if i == d_size:
                break
            else:             
                row_word = str(row).strip()
                if row_word != p:
                    dist = distance_ratio(p, row_word)
                    if len(hot_passes) < n:
                        hot_passes.append(row_word)
                        pass_dist.append(dist)
                    else:
                        d = min(pass_dist)
                        if dist > d:
                            ind = pass_dist.index(d)
                            hot_passes[ind] = row_word
                            pass_dist[ind] = dist
        return hot_passes
