
def count_instances(List): #IN: a list; OUT: a dictionary. its keys are the list elements, its values are the probability of a given element to be in the list

    s = [] #elements of List, without repetitions
    for elem in List:
        if elem not in s:
            s.append(elem)
    #print(List)
    l = len(List)
    d = {} # the dictionary
    for elem in s:
        c = 0 # count how many times elem is in List
        for i in range(l):
            if elem == List[i]:
                c += 1
        #print("{} -> {} ({})".format(elem, c, c/l))
        d[elem] = c/l
    #print(d)
    return d

def markov(file_in):
    lenghts = []
    M = []
    states = [] #will contain all the TLS message types seen in the flows

###################################################################
    with open(file_in) as f:
        row = 0
        for line in f.readlines():
            r = []
            if not line.startswith('stream') and not line.startswith('TAG') and not line.startswith('\n'):
                record = line.split()
                l = len(record)
                lenghts.append(l)
                for j in range(l):
                    r.append(record[j])
                    if record[j] not in states:
                        states.append(record[j])
                M.append(r)
                #print(r)
                row = row+1
###################################################################

    ALL = []

    #compute enter probability vector R
    enter = []
    for i in range(row):
        enter.append(M[i][0])
    R = count_instances(enter)
    ALL.append(R)

    #compute exit probability vector T
    exit = []
    for i in range(row):
        exit.append(M[i][lenghts[i]-1])
    T = count_instances(exit)
    #ALL.append(T)

    P = {}
    for s in states:
        #print("STATE '{}': ".format(s), end=" ")
        next_states = []
        for i in range(row):
            l = len(M[i])
            for j, elem in enumerate(M[i]):
                if s==elem and j+1 < l:
                    next_states.append(M[i][j+1])
        d = count_instances(next_states)
        P[s] = d

    ALL.append(P)
    ALL.append(T)
    #print(ALL)

    return ALL

#M = markov(file_in)
#M[0])enter
#M[1] transition
#M[2] exit
