
def enter_exit_probability(dict, state):
    # given Q or W, find corresponding state (key) and probability (value)
    try:
        #print(dict[state])
        return dict[state]
    except:
        print("{}: no corresponding state".format(state))
        return(0)
    
def transition_probability(P, X):
    l = len(X)
    v = []
    for i in range(l-1):
        try:
            p = P[X[i]][X[i+1]]
            v.append(p)
        except:
            p = 0
            v.append(p)
            print("{} -> {}: no corresponding state".format(X[i], X[i+1]))
    M = 1
    #print(v)
    for p in v:
        M = M*p
    #print("transition probability: {}".format(M))
    return M

def prob(R, P, T, X):
    #P == transition matrix
    #R == enter-probability distribution
    #T == exit-probability distribution
    #X == sequence of TLS message types
    r = enter_exit_probability(R, X[0])
    l = len(X)
    t = enter_exit_probability(T, X[l-1])
    p = transition_probability(P, X)

    prob = r * t * p
    return prob

####################### TEST #######################
#P = {'A': {'A': 0.25, 'B': 0.5, 'C': 0.25}, 'B': {'B': 0.25, 'C': 0.75}, 'C': {'C': 0.75, 'B': 0.25}}
#R = {'A': 0.75, 'B': 0.25}
#T = {'B': 0.25, 'C': 0.75}
#X = ['C', 'C', 'B', 'A'] #0
#X = ['A', 'A', 'B', 'B'] #0.005859375
#X = ['A', 'C', 'B', 'C'] #0.0263671875
#X = ['A', 'B', 'C', 'C'] #0.158203125
#X = ['B', 'B', 'B', 'B'] #0.0009765625
#X = ['A', 'B', 'B', 'A', 'C', 'C', 'C']
####################################################
#P = {'22:1': {'22:2': 0.3076923076923077, '22:2:11': 0.07692307692307693, '22:2:11:12:14': 0.15384615384615385, '22:2:11:14': 0.46153846153846156}, '22:2': {'22:11': 0.25, '20': 0.75}, '22:11': {'22:12': 1.0}, '22:12': {'22:16': 1.0}, '22:16': {'22:4': 1.0}, '22:4': {'23': 1.0}, '23': {'23': 1.0}, '22:2:11': {'22:12': 1.0}, '22:2:11:12:14': {'22:16': 1.0}, '20': {'23': 1.0}, '22:2:11:14': {'22:16': 1.0}}
#R = {'22:1': 1.0}
#T = {'23': 1.0}
#X = ['22:1', '22:2:11', '22:12', '22:16', '22:4', '23', '23', '23', '23']
####################################################

#p = (prob(R, P, T, X))
#print(p)
