import argparse
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

class MDP:
    def __init__(self, mdp_file):
        self.load_mdp(mdp_file)
        
    def load_mdp(self, mdp_file):
        # Read the MDP file and initialize the MDP instance
        with open(mdp_file, 'r') as f:
            lines = f.readlines()
        
        self.num_states = int(lines[0].split()[1])
        self.num_actions = int(lines[1].split()[1])
        self.start_state = int(lines[2].split()[1])
        self.end_states = [int(s) for s in lines[3].split()[1:]]

        self.transitions = {}
        for line in lines[4:-2]:
            s1, a, s2, r, p = map(float, line.split()[1:])
            self.transitions.setdefault((int(s1), int(a)), []).append((int(s2), r, p))

        self.mdptype = lines[-2].split()[1]
        self.discount = float(lines[-1].split()[1])

        # Initialize the value function and policy arrays
        self.V = [0.0] * self.num_states
        self.pi = [0] * self.num_states

    def value_iteration(self):
        # Implement Value Iteration to compute V* and π*
        epsilon = 1e-6
        while True:
            delta = 0.0
            for s in range(self.num_states):
                if s not in self.end_states:
                    v = self.V[s]
                    self.V[s] = max(self.q_value(s, a) for a in range(self.num_actions))
                    delta = max(delta, abs(self.V[s] - v))
            if delta < epsilon:
                break

        # Compute the optimal policy using the computed values
        self.compute_optimal_policy()

    def howards_policy_iteration(self):
        # Implement Howard's Policy Iteration to compute V* and π*
        self.pi = [0] * self.num_states  # Initialize the policy arbitrarily
        while True:
            self.policy_evaluation()
            policy_stable = True
            for s in range(self.num_states):
                if s not in self.end_states:
                    a = self.best_action(s)
                    if a != self.pi[s]:
                        policy_stable = False
                        self.pi[s] = a
            if policy_stable:
                break

    def linear_programming(self):
        # Implement Linear Programming to compute V* and π*
        model = LpProblem(name="MDP_LP", sense=LpMaximize)
        V = [LpVariable(name=f"V_{s}", lowBound=None) for s in range(self.num_states)]

        # Objective function
        model += lpSum(V[s] for s in range(self.num_states))

        # Constraints
        for s in range(self.num_states):
            if s in self.end_states:
                model += V[s] == 0.0
            else:
                q_values = [self.q_value(s, a) for a in range(self.num_actions)]
                model += V[s] >= lpSum(q_values)

        # Solve the linear program
        model.solve()

        # Extract the results
        for s in range(self.num_states):
            self.V[s] = V[s].value()

        # Compute the optimal policy using the computed values
        self.compute_optimal_policy()

    def policy_evaluation(self):
        epsilon = 1e-6
        while True:
            delta = 0.0
            for s in range(self.num_states):
                if s not in self.end_states:
                    v = self.V[s]
                    self.V[s] = self.q_value(s, self.pi[s])
                    delta = max(delta, abs(self.V[s] - v))
            if delta < epsilon:
                break

    def q_value(self, s, a):
        # Compute the Q-value for state s and action a
        q = 0.0
        for s2, r, p in self.transitions.get((s, a), []):
            q += p * (r + self.discount * self.V[s2])
        return q

    def best_action(self, s):
        # Find the best action for state s
        best_a, best_q = None, float('-inf')
        for a in range(self.num_actions):
            q = self.q_value(s, a)
            if q > best_q:
                best_q = q
                best_a = a
        return best_a

    def compute_optimal_policy(self):
        # Compute the optimal policy using the computed values
        for s in range(self.num_states):
            if s not in self.end_states:
                self.pi[s] = self.best_action(s)

    def solve(self, algorithm):
        if algorithm == 'vi':
            self.value_iteration()
        elif algorithm == 'hpi':
            self.howards_policy_iteration()
        elif algorithm == 'lp':
            self.linear_programming()
        else:
            print("Invalid algorithm selected. Please choose one of 'vi', 'hpi', or 'lp'.")

    def print_results(self):
        # Print the results in the desired format
        for s in range(self.num_states):
            v_star, pi_star = self.V[s], self.pi[s]
            print(f"{v_star:.6f}\t{pi_star}")

def main():
    parser = argparse.ArgumentParser(description="MDP Planning Algorithms")
    parser.add_argument("--mdp", type=str, help="Path to the input MDP file")
    parser.add_argument("--algorithm", type=str, choices=["vi", "hpi", "lp"], help="Algorithm to use: vi, hpi, or lp")
    args = parser.parse_args()

    if not args.mdp or not args.algorithm:
        print("Both --mdp and --algorithm arguments are required.")
        return

    mdp = MDP(args.mdp)
    mdp.solve(args.algorithm)
    mdp.print_results()

if __name__ == "__main__":
    main()
