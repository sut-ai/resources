import numpy as np

def find_prob (seq, level, last_state = None ):
    if len(seq) == 1:
        ##### sum  p(y1 | x1) * p (x1) on x1
        return  np.sum(obs[:,seq[0]] * pi)
    if len(seq) == level:
        #### sum p(yk|xk) * p(xk|x(k-1)) on xk
        return np.sum(obs[:,seq[level-1]] * transitions[last_state][:])
    result = 0
    for state in range(num_of_states):
        emission = seq[level - 1]
        if level == 1:
            result += pi[state] * obs[state,emission] * find_prob(seq, level+1, last_state= state)
        else:
            result += transitions[last_state,state] * obs[state,emission] * find_prob(seq, level+1, last_state= state)
    return result



transitions = np.array( [[0,1,0,0,0,0,0,0],
               [0,0,1,0,0,0,0,0],
               [0,0,0,0.4,0,0,0.6,0],
               [0,0,0,0,1,0,0,0],
               [0,0,0,0,0,1,0,0],
               [0,0,0,0,0,0,0,1],
               [0,0,0,0.6,0,0,0.4,0],
               [0,0,0,0,0,0,0,1]])

obs = np.array([[0.8,0,0,0.2],
       [0,0.8,0.2,0],
       [0.8,0.2,0,0],
       [1 ,0, 0, 0] ,
       [0,0,0.2,0.8],
       [0,0.8,0.2,0],
       [0.2,0.2,0.4,0.2],
       [0.25,0.25,0.25,0.25]])

### p(x1 = L_j ) = 1/8   initial state probabilities are same for 8 states
pi = [1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8 ]

DNA_dict = {'A': 0, 'C':1, 'G':2, 'T':3}
DNA_string = input()
sequence = [DNA_dict[character] for character in DNA_string]

num_of_states = 8

likelihood = find_prob(sequence, level=1)

score = likelihood / ((0.25)**len(sequence))

print('score: ', score)




