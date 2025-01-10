
def count_instances(List): #IN: a list; OUT: a dictionary. its keys are the list elements, its values are the probability of a given element to be in the list

    s = [] #elements of List, without repetitions
    for elem in List:
        if elem not in s:
            s.append(elem)
    #print(List)
    l = len(List)
    d = {} # dictionary
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
    M = [] #will contain all the type sequences
    states = [] #will contain all the TLS message types (i.e. states) seen in the flows

    ###################################################################
    with open(file_in) as f:
        row = 0 # cont the number of type sequences, or rows in the transition matrix
        for line in f.readlines():
            r = []
            if not line.startswith('stream') and not line.startswith('TAG') and not line.startswith('\n'): # get only the type sequences
                record = line.split() #the type sequence
                l = len(record)
                lenghts.append(l)
                for j in range(l):
                    r.append(record[j])
                    if record[j] not in states: #if a new state is found, add it to states
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

    #compute transition matrix
    P = {}
    for s in states:
        #print("STATE '{}': ".format(s), end=" ")
        next_states = [] #
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

#ALL[0] enter
#ALL[1] transition
#ALL[2] exit
