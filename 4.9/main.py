#!/usr/bin/python3

import pickle
import seaborn

class ValueIteration:

    def __init__(self, ph = .4, win_state = 100):
        # state is the amount of money held by the player
        self.win_state = win_state
        # value of each state is the probability of winning with that much money
        self.V = [0 for _ in range(win_state + 1)] # also account for state=0
        # once player reaches 100, the win is definite
        self.V[-1] = 0

        # policy is the best action to take
        self.P = [0 for _ in range(win_state+1)]

        self.ph = ph

    # s is the state: amount of money held
    def updateV(self, s):
        best_action, best_outcome = 0, 0
        # action is the value of the bet; it can go from 1 to s
        for a in range(0, min(s, self.win_state-s)):
            new_state_value = 0
            
            # lose
            next_state = max(0, s-a)
            reward = 0
            new_state_value += (1-self.ph) * (reward + self.V[next_state])

            # win
            next_state = min(100, s+a)
            reward = 1 if s+a >= self.win_state else 0
            new_state_value += self.ph * (reward + self.V[next_state])

            if best_outcome < new_state_value:
                best_action, best_outcome = a, new_state_value
            
        #print(f"state {s}, best action {best_action}, best value {best_outcome}")
        
        delta = abs(self.V[s]-best_outcome)
        self.V[s] = best_outcome
        self.P[s] = best_action

        return delta

    def updateS(self):
        delta = 0
        for s in range(1, self.win_state+1):
            delta = max(delta, self.updateV(s))
        return delta

    def loop(self, stop_delta=.000001, stop_iterations=100000):
        for i in range(stop_iterations):
            delta = self.updateS()
            print(f"iteration {i}, delta {delta}")
            if delta < stop_delta:
                break

    def save(self, path):
        with open(path, "wb") as output:
            pickle.dump((self.V, self.P, self.ph), output)

    def load(self, path):
        with open(path, "rb") as input:
            self.V, self.P, self.ph = pickle.load(input)

    def print(self):
        for s in range(1, self.win_state):
            print("state {}: {:.5f}, {}".format(s, self.V[s], self.P[s]))


if __name__ == '__main__':
    vi = ValueIteration()
    vi.loop()
    vi.print()
