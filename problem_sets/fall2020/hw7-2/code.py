# credits go to Mr. Masih Eskandar (masih.eskandar@gmail.com)
import random
import time
import gym
import numpy as np

env = gym.make('MountainCar-v0')
num_actions = 3

num_states = 190000  # number of discrete states(enter your desire number)

q_table = np.zeros(shape=(num_states, num_actions))
min_p = -1.2
min_v = -0.07
gamma = 1


# you may change the inputs of any function as you desire.


def discretize_state(x, min, step):
    """
    this is just one example of a discretization function. you can change it as you want:)
    """
    return int((x - min) / step)


def env_state_to_Q_state(state):
    [position, velocity] = state
    """
    return value: [int]
    your code here. 
    hint: use discretize_state func here for both of p and v and combine them somehow to reach a int.
    """
    return discretize_state(position, min_p, 0.01) * 1000 + discretize_state(velocity, min_v, 0.001)


def update_q(q_table, state, action, reward, s_p, alpha):
    """ your code here"""
    sample = reward + np.amax(q_table[s_p]) * gamma
    q_table[state][action] = q_table[state][action] * (1 - alpha) + alpha * sample


def get_action(q_table, state, epsilon):
    """your code here"""
    p = np.random.random()
    if p < epsilon:
        return np.random.choice([0, 1, 2])
    else:
        return np.argmax(q_table[state])


def q_learning(episodes, alpha):
    """your code here"""
    scores = []
    epsilon = 1
    for episode in range(episodes):
        # print('******Training Episode ', episode)
        state, score, done, step = env_state_to_Q_state(env.reset()), 0, False, 0
        while not done:
            # if episode > 4000:
            #     time.sleep(0.04)
            action = get_action(q_table, state, epsilon=epsilon)
            state_p, reward, done, _ = env.step(action)
            state_p = env_state_to_Q_state(state_p)
            update_q(q_table, state, action, reward, state_p, alpha)
            state = state_p
            score += int(reward)
            # if episode > 4000:
            #     env.render()
        # print('Score:', score)
        scores.append(score)
        epsilon -= epsilon / episodes
        if epsilon < 0:
            epsilon = 0
        if (episode + 1) % 5000 == 0:
            print("Episode", episode + 1, "/", episodes)
    # print("Average score over", episodes, "run : ", np.array(scores).mean())


def save_policy():
    """save your optimal policy to a file with name policy.npy"""
    np.save("./policy", np.argmax(q_table, axis=1))


# attention: don't change this function. we will use this to grade your policy which you will hand in with policy.npy
# btw you can use it to see how you are performing. uncomment two lines which are commented to be able to see what is happening visually
def score():
    policy, scores = np.load("./policy.npy"), []
    # print(policy)
    for episode in range(1000):
        print('******Episode ', episode)
        state, score, done, step = env_state_to_Q_state(env.reset()), 0, False, 0
        while not done:
            # time.sleep(0.04)
            action = policy[state]
            state, reward, done, _ = env.step(action)
            state = env_state_to_Q_state(state)
            step += 1
            score += int(reward)
            # env.render()
        print('Score:', score)
        scores.append(score)
    print("Average score over 1000 run : ", np.array(scores).mean())


if __name__ == '__main__':
    print("Commencing training!")
    q_learning(100000, 0.6)
    print("Training complete!")
    save_policy()
    score()
