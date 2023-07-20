import argparse

class MazeEncoder:
    def __init__(self, grid_file):
        self.grid = self.load_grid(grid_file)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.mdp = []
        self.actions = ["N", "S", "E", "W"]

    def load_grid(self, grid_file):
        # Read the maze grid from the file
        with open(grid_file, 'r') as f:
            grid = [list(line.strip()) for line in f.readlines()]
        return grid

    def state_to_id(self, row, col):
        # Convert the (row, col) position to a unique state ID
        return row * self.num_cols + col

    def is_valid_move(self, row, col, action):
        # Check if the move is valid (doesn't hit a wall)
        if action == "N" and row > 0 and self.grid[row - 1][col] != "1":
            return True
        elif action == "S" and row < self.num_rows - 1 and self.grid[row + 1][col] != "1":
            return True
        elif action == "E" and col < self.num_cols - 1 and self.grid[row][col + 1] != "1":
            return True
        elif action == "W" and col > 0 and self.grid[row][col - 1] != "1":
            return True
        return False

    def encode_mdp(self):
        # Encode the maze as an MDP
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                state = self.state_to_id(row, col)
                if self.grid[row][col] == "3":
                    # End state
                    self.mdp.append(f"numStates 1\nnumActions 1\nstart {state}\nend {state}\n")
                elif self.grid[row][col] != "1":
                    # Non-wall state
                    num_actions = 0
                    for action in self.actions:
                        if self.is_valid_move(row, col, action):
                            num_actions += 1
                            next_row, next_col = self.get_next_position(row, col, action)
                            next_state = self.state_to_id(next_row, next_col)
                            self.mdp.append(f"transition {state} {action} {next_state} 0.0 1.0\n")
                    self.mdp.append(f"numStates 1\nnumActions {num_actions}\nstart {state}\nend -1\n")

    def get_next_position(self, row, col, action):
        # Get the next position based on the action
        if action == "N":
            return row - 1, col
        elif action == "S":
            return row + 1, col
        elif action == "E":
            return row, col + 1
        elif action == "W":
            return row, col - 1

    def print_mdp(self):
        # Print the MDP in the desired format
        for line in self.mdp:
            print(line, end="")

def main():
    parser = argparse.ArgumentParser(description="Maze Encoder")
    parser.add_argument("--grid", type=str, help="Path to the input maze grid file")
    args = parser.parse_args()

    if not args.grid:
        print("Please provide the --grid argument with the path to the maze grid file.")
        return

    encoder = MazeEncoder(args.grid)
    encoder.encode_mdp()
    encoder.print_mdp()

if __name__ == "__main__":
    main()