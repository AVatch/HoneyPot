import numpy as np
from rock_you_generator import distance_ratio

def loadtxt(f):
    password = np.loadtxt(f,
                          delimiter='\n',
                          dtype={
                                 'names': ('password',),
                                 'formats': ('S99',)},
                          unpack=True)
    return password

# Load data
pass_file = loadtxt("group1/1")


# Create similiarity matrix
pass_matrix = [[] for x in range(0, len(pass_file))]

for i in range(len(pass_file)):
    for j in range(len(pass_file)):
        dist = distance_ratio(pass_file[i][0], pass_file[j][0])
        pass_matrix[i].append(dist)

print "*"*50
print '\t00, 01, 02, 03, 04, 05, 06, 07, 08, 09'
for i in range(len(pass_matrix)):
    print i, '\t', pass_matrix[i]

# Pull out pairs of similiar entries
threshold = 80
pairs = []
for i in range(len(pass_matrix)):
    for j in range(len(pass_matrix[i])):
        if pass_matrix[i][j] >= threshold and pass_matrix[i][j] != 100:
            p1 = pass_file[i][0]
            p2 = pass_file[j][0]
            pollen = [p1, p2, pass_matrix[i][j]]
            redundant_pollen = [p2, p1, pass_matrix[i][j]]
            if pollen not in pairs and redundant_pollen not in pairs:
                pairs.append(pollen)

print "*"*50
print "Above threshold: ", threshold
for i in pairs:
    print i
