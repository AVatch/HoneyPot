import sys
import random
import honey_functions as hf

'''
Main Functions
'''

def pollinateMe(p, k):
    pot = [p]
    buckets = random.randrange(1,k)
    while (k % buckets):
        buckets = random.randrange(1,k)
    count = k/buckets
    for i in range(0,buckets) :
        seed = random.choice(pot)
        for j in range(0,count) :
            weight = random.random()
            func = random.choice(hf.FUNCTIONS)
            honey = func(seed,weight)
            while honey in pot:
                func = random.choice(hf.FUNCTIONS)
                honey = func(seed,weight)
            pot.append(honey)

    random.shuffle(pot)
    return pot


def unPollinateMe(p, k):
    pass


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
        print 'HONEY WORDS:\n', "\n".join(words)
    elif action == 'unpollinate':
        print 'un-pollinating'
    else:
        print "unknown action"
