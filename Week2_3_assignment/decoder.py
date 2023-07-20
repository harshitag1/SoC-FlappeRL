import argparse

class MazeDecoder:
    def __init__(self, grid_file, value_policy_file):
        self.grid = self.load_grid(grid_file)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.value_policy = self.load_value_policy(value_policy_file)
        self.actions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

    def load_grid(self, grid_file):
        # Read the maze grid from the file
        with open(grid_file, 'r') as f:
            grid = [list(line.strip()) for line in f.readlines()]
        return grid

    def load_value_policy(self, value_policy_file):
        # Read the value function and policy from the file
        with open(value_policy_file, 'r') as f:
            lines = f.readlines()

        value_policy = {}
        for line in lines:
            state, value, policy = line.strip().split()
            value_policy[int(state)] = (float(value), policy)
        return value_policy

    def state_to_id(self, row, col):
        # Convert the (row, col) position to a unique state ID
        return row * self.num_cols + col

    def simulate_policy(self):
        # Simulate the optimal policy and find the path from start to end
        start_state = self.get_start_state()
        current_state = start_state
        path = []

        while current_state not in self.get_end_states():
            _, policy = self.value_policy[current_state]
            path.append(policy)
            action = self.actions[policy]
            next_state = self.get_next_state(current_state, action)
            current_state = next_state

        return path

    def get_start_state(self):
        # Find the start state in the value_policy dictionary
        for state, (_, policy) in self.value_policy.items():
            if policy == "start":
                return state

    def get_end_states(self):
        # Find the end states in the value_policy dictionary
        end_states = set()
        for state, (_, policy) in self.value_policy.items():
            if policy == "end":
                end_states.add(state)
        return end_states

    def get_next_state(self, state, action):
        # Get the next state based on the action
        next_row = state // self.num_cols + action[0]
        next_col = state % self.num_cols + action[1]
        if 0 <= next_row < self.num_rows and 0 <= next_col < self.num_cols and self.grid[next_row][next_col] != "1":
            return self.state_to_id(next_row, next_col)
        return state

def main():
    parser = argparse.ArgumentParser(description="Maze Decoder")
    parser.add_argument("--grid", type=str, help="Path to the input maze grid file")
    parser.add_argument("--value_policy", type=str, help="Path to the value and policy file")
    args = parser.parse_args()

    if not args.grid or not args.value_policy:
        print("Both --grid and --value_policy arguments are required.")
        return

    decoder = MazeDecoder(args.grid, args.value_policy)
    path = decoder.simulate_policy()
    print(" ".join(path))

if __name__ == "__main__":
    main()