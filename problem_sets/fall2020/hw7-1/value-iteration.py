import numpy as np


actions = [[-1, 0], [1, 0], [0, -1], [0, 1]]


def get_n_state(states, is_obstacle, c_row, c_col, n_row, n_col):
    rows, cols = states.shape
    if n_row < 0 or n_row >= rows:
        return states[c_row, c_col]
    if n_col < 0 or n_col >= cols:
        return states[c_row, c_col]
    if is_obstacle[n_row, n_col]:
        return states[c_row, c_col]
    return states[n_row, n_col]



def valueiteration(rewards, ware, nofly):
    states_str = np.array(rewards, dtype='S')
    states = np.zeros(states_str.shape, dtype=float)
    is_terminal = np.zeros(states.shape)
    is_obstacle = np.zeros(states.shape)
    
    rows, cols = states.shape
    for pos in ware:
        is_terminal[pos[0], pos[1]] = 1
    for pos in nofly:
        is_terminal[pos[0], pos[1]] = 1
    for i in range(rows):
        for j in range(cols):
            if states_str[i, j] == 'None':
                is_obstacle[i, j] = 1
            else:
                states[i, j] = float(rewards[i][j])
            

    sigma = 10
    discount = 0.9
    ans = list()

    while sigma > 0.001 * discount * (1 - discount):
        n_states = states.copy()
        sigma = 0

        for i in range(rows):
            for j in range(cols):
                if is_terminal[i, j]:
                    continue
                if is_obstacle[i, j]:
                    continue

                # print("pos:", i, j)
                best_value = float('-inf')
                for a_index in range(4):
                    tmp_value = 0
                    
                    # desired action
                    action = actions[a_index]
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(states, is_obstacle, i, j, n_row, n_col) * 0.9
                    # print("next state:", n_state)
                    tmp_value += (float(rewards[i][j]) + n_state) * 0.8

                    # noisy action to left
                    if a_index < 2:
                        action = actions[2]
                    else:
                        action = actions[0]
                    # print("action left:", action)
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(states, is_obstacle, i, j, n_row, n_col) * 0.9
                    # print("next state:", n_state)
                    tmp_value += (float(rewards[i][j]) + n_state) * 0.1

                    # noisy action to right
                    if a_index < 2:
                        action = actions[3]
                    else:
                        action = actions[1]
                    # print("action right:", action)
                    n_row = i + action[0]
                    n_col = j + action[1]
                    n_state = get_n_state(states, is_obstacle, i, j, n_row, n_col) * 0.9
                    # print("next state:", n_state)
                    tmp_value += (float(rewards[i][j]) + n_state) * 0.1

                    # print("tmp value:", tmp_value)
                    if tmp_value > best_value:
                        best_value = tmp_value
               
                sigma = max(sigma, abs(best_value - states[i, j]))
                n_states[i, j] = best_value
        
        states = n_states
        ansi = list()
        for i in range(rows):
            for j in range(cols):
                if is_obstacle[i, j]:
                    ansi.append('None')
                else:
                    ansi.append(str(states[i, j]))
        ans.append(ansi)
    
    # policy extraction
    actions_str = ['N', 'S', 'W', 'E']
    optimal_policy = list()
    for i in range(rows):
        for j in range(cols):
            if is_terminal[i, j]:
                optimal_policy.append('None')
                continue
            if is_obstacle[i, j]:
                optimal_policy.append('None')
                continue

            best_value = float('-inf')
            best_action = 'X'
            for a_index in range(4):
                tmp_value = 0
                
                # desired action
                action = actions[a_index]
                n_row = i + action[0]
                n_col = j + action[1]
                n_state = get_n_state(states, is_obstacle, i, j, n_row, n_col) * 0.9
                tmp_value += n_state * 0.8

                # noisy action to left
                if a_index < 2:
                    action = actions[2]
                else:
                    action = actions[0]
                n_row = i + action[0]
                n_col = j + action[1]
                n_state = get_n_state(states, is_obstacle, i, j, n_row, n_col) * 0.9
                tmp_value += n_state * 0.1

                # noisy action to right
                if a_index < 2:
                    action = actions[3]
                else:
                    action = actions[1]
                n_row = i + action[0]
                n_col = j + action[1]
                n_state = get_n_state(states, is_obstacle, i, j, n_row, n_col) * 0.9
                tmp_value += n_state * 0.1

                if tmp_value > best_value:
                    best_value = tmp_value
                    best_action = actions_str[a_index]
            optimal_policy.append(best_action)
    
    return ans, optimal_policy

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
out = valueiteration(mdp, ware, nofly)
print(out)
# for val in out[0]:
#     print(val)
# print(out[1])




