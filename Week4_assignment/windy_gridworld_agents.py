import numpy as np
import random
import matplotlib.pyplot as plt

class WindyGridworld:
    def __init__(self, rows, cols, wind_strength):
        self.rows = rows
        self.cols = cols
        self.wind_strength = wind_strength

        self.start_state = (3, 0)
        self.goal_state = (3, 7)

        self.actions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]

    def step(self, state, action):
        next_state = (state[0] + action[0], state[1] + action[1] + self.wind_strength[state[1]])
        next_state = (max(0, min(self.rows - 1, next_state[0])),
                      max(0, min(self.cols - 1, next_state[1])))

        reward = -1
        if next_state == self.goal_state:
            reward = 0

        return next_state, reward

def epsilon_greedy_action(Q, state, epsilon):
    if random.random() < epsilon:
        return random.choice(range(len(Q[state])))
    else:
        return np.argmax(Q[state])

def sarsa_zero(agent, num_episodes, alpha, epsilon, gamma):
    Q = np.zeros((agent.rows, agent.cols, len(agent.actions)))
    episode_steps = []

    for _ in range(num_episodes):
        state = agent.start_state
        action = epsilon_greedy_action(Q, state, epsilon)
        steps = 0

        while state != agent.goal_state:
            next_state, reward = agent.step(state, agent.actions[action])
            next_action = epsilon_greedy_action(Q, next_state, epsilon)
            Q[state][action] += alpha * (reward + gamma * Q[next_state][next_action] - Q[state][action])

            state = next_state
            action = next_action
            steps += 1

        episode_steps.append(steps)

    return episode_steps, Q

def expected_sarsa(agent, num_episodes, alpha, epsilon, gamma):
    Q = np.zeros((agent.rows, agent.cols, len(agent.actions)))
    episode_steps = []

    for _ in range(num_episodes):
        state = agent.start_state
        steps = 0

        while state != agent.goal_state:
            action = epsilon_greedy_action(Q, state, epsilon)
            next_state, reward = agent.step(state, agent.actions[action])

            expected_value = sum(Q[next_state]) / len(Q[next_state])
            Q[state][action] += alpha * (reward + gamma * expected_value - Q[state][action])

            state = next_state
            steps += 1

        episode_steps.append(steps)

    return episode_steps, Q

def q_learning(agent, num_episodes, alpha, epsilon, gamma):
    Q = np.zeros((agent.rows, agent.cols, len(agent.actions)))
    episode_steps = []

    for _ in range(num_episodes):
        state = agent.start_state
        steps = 0

        while state != agent.goal_state:
            action = epsilon_greedy_action(Q, state, epsilon)
            next_state, reward = agent.step(state, agent.actions[action])

            max_next_value = max(Q[next_state])
            Q[state][action] += alpha * (reward + gamma * max_next_value - Q[state][action])

            state = next_state
            steps += 1

        episode_steps.append(steps)

    return episode_steps, Q

def plot_episodes_vs_steps(episodes_vs_steps_sarsa, episodes_vs_steps_exp_sarsa, episodes_vs_steps_q_learning):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(episodes_vs_steps_sarsa)), episodes_vs_steps_sarsa, label='Sarsa(0)')
    plt.plot(range(len(episodes_vs_steps_exp_sarsa)), episodes_vs_steps_exp_sarsa, label='Expected Sarsa')
    plt.plot(range(len(episodes_vs_steps_q_learning)), episodes_vs_steps_q_learning, label='Q-learning')
    plt.xlabel('Episodes')
    plt.ylabel('Time Steps')
    plt.legend()
    plt.title('Episodes vs Time Steps')
    plt.show()

if __name__ == "__main__":
    # Windy Gridworld parameters
    rows = 7
    cols = 10
    wind_strength = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

    agent = WindyGridworld(rows, cols, wind_strength)

    num_episodes = 200
    alpha = 0.1
    epsilon = 0.1
    gamma = 1.0

    num_runs = 10
    episodes_vs_steps_sarsa = []
    episodes_vs_steps_exp_sarsa = []
    episodes_vs_steps_q_learning = []

    for _ in range(num_runs):
        steps_sarsa, _ = sarsa_zero(agent, num_episodes, alpha, epsilon, gamma)
        episodes_vs_steps_sarsa.append(steps_sarsa)

        steps_exp_sarsa, _ = expected_sarsa(agent, num_episodes, alpha, epsilon, gamma)
        episodes_vs_steps_exp_sarsa.append(steps_exp_sarsa)

        steps_q_learning, _ = q_learning(agent, num_episodes, alpha, epsilon, gamma)
        episodes_vs_steps_q_learning.append(steps_q_learning)

    episodes_vs_steps_sarsa_avg = np.mean(episodes_vs_steps_sarsa, axis=0)
    episodes_vs_steps_exp_sarsa_avg = np.mean(episodes_vs_steps_exp_sarsa, axis=0)
    episodes_vs_steps_q_learning_avg = np.mean(episodes_vs_steps_q_learning, axis=0)

    plot_episodes_vs_steps(episodes_vs_steps_sarsa_avg, episodes_vs_steps_exp_sarsa_avg, episodes_vs_steps_q_learning_avg)