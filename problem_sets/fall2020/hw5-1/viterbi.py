import numpy as np

def viterbi(seq, trans, obs, Pi):
    """
    Parameters
    ----------
    seq : array (K,)
        Observation state sequence.
    trans : array (8, 8)
        State transition matrix.
        details.
    obs : array (8, 4)
        Emission matrix.
    Pi: (8,)
        Initial state probabilities: Pi[i] is the probability x_1 == i.

    Returns
    -------
    x : array (K,)
        Most likely path of hidden states,
        conditioned on observation sequence y under the model parameters A, B,
        Pi.
    T1: array (num_of_states, K)
        the probability of the most likely path so far
    T2: array (num_of_states, K)
        the x_j-1 of the most likely path so far
    """
    num_of_states = 8
    K = len(seq)

    T1 = np.empty((num_of_states, K), 'd')
    T2 = np.empty((num_of_states, K), 'B')

    # Initialize the tracking tables from first observation
    T1[:, 0] = Pi * obs[:, seq[0]]
    T2[:, 0] = 0

    # Iterate through the observations updating the tracking tables
    for i in range(1, K):
        T1[:, i] = np.max(T1[:, i - 1] * trans.T * obs[np.newaxis, :, seq[i]].T, 1)
        T2[:, i] = np.argmax(T1[:, i - 1] * trans.T, 1)

    # Build the output, optimal path
    x = np.empty(K, 'B')
    x[-1] = np.argmax(T1[:, K - 1])
    for i in reversed(range(1, K)):
        x[i - 1] = T2[x[i], i]

    return x, T1, T2



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

x, T1, T2 = viterbi(sequence, transitions, obs, pi)

state_dict = {0: 'l_1',1: 'l_2', 2: 'l_3',3: 'l_4', 4: 'l_5',5: 'l_6', 6: 'l_i',7: 'l_f'}

path = [state_dict[s] for s in x]
print(path)
maximum = np.max(T1, axis=0)[-1]
print(maximum)


