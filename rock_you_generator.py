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


def rock_you_like_a_hurricane(p, n, d_size):
    hot_passes = []
    pass_dist = []
    f = open('rockyou_clean.csv', 'r')
    try:
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            if row[0] != p:
                if i == d_size:
                    break
                dist = distance_ratio(p, str(row[0]))
                if len(hot_passes) < n:
                    hot_passes.append(str(row[0]))
                    pass_dist.append(dist)
                else:
                    d = min(pass_dist)
                    if dist > d:
                        i = pass_dist.index(d)
                        hot_passes[i] = str(row[0])
                        pass_dist[i] = dist
        return hot_passes
    finally:
        f.close()
