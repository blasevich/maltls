
def enter_exit_probability(dict, state):
    # given Q or W, find corresponding state (key) and probability (value)
    try:
        #print(dict[state])
        return dict[state]
    except:
        print("{}: no corresponding state".format(state))
        return 0
    
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

