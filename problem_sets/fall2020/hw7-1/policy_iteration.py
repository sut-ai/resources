import numpy as np

actions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
actions_str = ['N', 'S', 'W', 'E']


def get_n_state(states, is_obstacle, c_row, c_col, n_row, n_col):
    rows, cols = states.shape
    if n_row < 0 or n_row >= rows:
        return states[c_row, c_col]
    if n_col < 0 or n_col >= cols:
        return states[c_row, c_col]
    if is_obstacle[n_row, n_col]:
        return states[c_row, c_col]
    return states[n_row, n_col]



def policyiteration(rewards, ware, nofly):
    states_str = np.array(rewards, dtype='S')
    states = np.zeros(states_str.shape, dtype=float)
    is_terminal = np.zeros(states.shape)
    is_obstacle = np.zeros(states.shape)
    rows, cols = states.shape
    policy = [['N' for j in range(cols)] for i in range(rows)]
    ans = list()
    ansi = list()


    for pos in ware:
        is_terminal[pos[0], pos[1]] = 1
        policy[pos[0]][pos[1]] = 'None'
    for pos in nofly:
        is_terminal[pos[0], pos[1]] = 1
        policy[pos[0]][pos[1]] = 'None'
    for i in range(rows):
        for j in range(cols):
            if states_str[i, j] == 'None':
                is_obstacle[i, j] = 1
                policy[i][j] = 'None'
            else:
                states[i, j] = float(rewards[i][j])
            ansi.append(policy[i][j])
    ans.append(ansi)
    
    
    discount = 0.9
    diff = 1

    while diff > 0:
        diff = 0

        # policy evaluation
        c_states = states.copy()
        sigma = 10

        while sigma > 0.001 * discount * (1 - discount):
            n_states = c_states.copy()
            sigma = 0

            for i in range(rows):
                for j in range(cols):
                    if is_terminal[i, j]:
                        continue
                    if is_obstacle[i, j]:
                        continue

                    value = 0
                    if policy[i][j] == 'N':
                        a_index = 0
                    elif policy[i][j] == 'S':
                        a_index = 1
                    elif policy[i][j] == 'W':
                        a_index = 2
                    else:
                        a_index = 3

                    # desired action
                    action = actions[a_index]
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(c_states, is_obstacle, i, j, n_row, n_col) * 0.9
                    value += (float(rewards[i][j]) + n_state) * 0.8

                    # noisy action to left
                    if a_index < 2:
                        action = actions[2]
                    else:
                        action = actions[0]
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(c_states, is_obstacle, i, j, n_row, n_col) * 0.9
                    value += (float(rewards[i][j]) + n_state) * 0.1

                    # noisy action to right
                    if a_index < 2:
                        action = actions[3]
                    else:
                        action = actions[1]
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(c_states, is_obstacle, i, j, n_row, n_col) * 0.9
                    value += (float(rewards[i][j]) + n_state) * 0.1
                
                    sigma = max(sigma, abs(value - c_states[i, j]))
                    n_states[i, j] = value
            c_states = n_states

        ansi = list()
        #policy update
        for i in range(rows):
            for j in range(cols):
                if policy[i][j] == 'None':
                    ansi.append('None')
                    continue

                best_value = float('-inf')
                best_action = 'X'
                for a_index in range(4):
                    tmp_value = 0
                    
                    # desired action
                    action = actions[a_index]
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(c_states, is_obstacle, i, j, n_row, n_col) * 0.9
                    tmp_value += (float(rewards[i][j]) + n_state) * 0.8

                    # noisy action to left
                    if a_index < 2:
                        action = actions[2]
                    else:
                        action = actions[0]
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(c_states, is_obstacle, i, j, n_row, n_col) * 0.9
                    tmp_value += (float(rewards[i][j]) + n_state) * 0.1

                    # noisy action to right
                    if a_index < 2:
                        action = actions[3]
                    else:
                        action = actions[1]
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(c_states, is_obstacle, i, j, n_row, n_col) * 0.9
                    tmp_value += (float(rewards[i][j]) + n_state) * 0.1

                    if tmp_value > best_value:
                        best_value = tmp_value
                        best_action = actions_str[a_index]
            
                if policy[i][j] != best_action:
                    diff += 1
                policy[i][j] = best_action
                ansi.append(best_action)
        
        ans.append(ansi)
    
    return ans        
        

n, m = map(int, input().split())
mdp = []
for i in range(n):
    mdpi = [a for a in input().split()]
    mdp.append(mdpi)

w = int(input())
ware_raw = [int(a) for a in input().split()]
ware = []
for i in range(w):
    ware.append([ware_raw[2*i], ware_raw[2*i + 1]])


nf = int(input())
nofly_raw = [int(a) for a in input().split()]
nofly = []
for i in range(nf):
    nofly.append([nofly_raw[2*i], nofly_raw[2*i+1]])

print(mdp)
print("-"*100)
print(ware)
print("-"*100)
print(nofly)

print("output:")
out = policyiteration(mdp, ware, nofly)
print(out)
# for val in out:
#     print(val)
