import random
import numpy as np

class MyChain:
    def __init__(self, probs):
        self.probs = probs
        self.states = list(probs.keys())
        print(f"State Keys: {self.states}")

    def get_next_state(self, current_state):
        next_state_weights = list(self.probs[current_state].values())
        next_states = self.states
        next_state = random.choices(next_states, weights=next_state_weights)[0]
        return next_state

transition_probabilities = {
    'X': {'X': 1.0, 'Y': 0.0, 'Z': 0.0, 'W': 0.0},
    'Y': {'X': 0.5, 'Y': 0.0, 'Z': 0.5, 'W': 0.0},
    'Z': {'X': 0.0, 'Y': 0.2, 'Z': 0.0, 'W': 0.8},
    'W': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'W': 1.0},
}

chain = MyChain(transition_probabilities)

current = 'Y'
counter = 0
while counter < 10:
    print(current)
    current = chain.get_next_state(current)
    counter += 1

transition_matrix = np.array([[1.0, 0.0, 0.0, 0.0],
                              [0.5, 0.0, 0.5, 0.0],
                              [0.0, 0.2, 0.0, 0.8],
                              [0.0, 0.0, 0.0, 1.0]])

# Define the starting state, target state, and number of steps
start_state = 1
target_state = 2
num_steps = 5

# Calculate the probability of reaching the target state from the starting state in the given number of steps
result_matrix = np.linalg.matrix_power(transition_matrix, num_steps)
probability = result_matrix[start_state, target_state]

# Print the probability as a percentage
print("The probability of reaching state {} from state {} in {} steps is {:.2%}".format(target_state + 1, start_state + 1, num_steps, probability))
