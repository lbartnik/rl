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
        #self.V[-1] = 1

        # policy is the best action to take
        self.P = [0 for _ in range(win_state+1)]
        self.ph = ph

    def possible_actions(self, s):
        values = []
        # action is the value of the bet; it can go from 1 to s
        actions = list(range(0, min(s, self.win_state-s)+1))
        for a in actions:
            new_state_value = 0
            
            # lose
            next_state = max(0, s-a)
            reward = 0
            new_state_value += (1-self.ph) * (reward + self.V[next_state])

            # win
            next_state = min(100, s+a)
            reward = 1 if s+a >= self.win_state else 0
            new_state_value += self.ph * (reward + self.V[next_state])
            
            values.append(new_state_value)
        return values
    
    def best_action(self, s):
        best_actions, best_value = self.best_actions(s)
        #return random.choice(best_actions), best_value
        # if only one choice
        if len(best_actions) == 1:
            return best_actions[0], best_value
        # if two choices, don't pick action zero
        if len(best_actions) == 2:
            if best_actions[0] == 0:
                return best_actions[1], best_value
            else:
                return best_actions[0], best_value
        # if multiple actions, don't pick zero nor the last one
        return best_actions[1], best_value
            
    def best_actions(self, s, eps=1e-9):
        values = self.possible_actions(s)
        best_value = max(values)
        return list(map(lambda x: x[0], filter(lambda x: abs(x[1]-best_value) < eps, enumerate(values)))), best_value
    
    def equal_policies(self):
        ans = []
        for s in range(1, self.win_state):
            best_actions, _ = self.best_actions(s)
            for a in best_actions:
                ans.append([s, a])
        return map(list, zip(*ans))
    
    # s is the state: amount of money held
    def updateV(self, s):
        best_action, best_value = self.best_action(s)
        
        delta = abs(self.V[s]-best_value)
        self.V[s] = best_value
        self.P[s] = best_action

        return delta

    def updateS(self):
        delta = 0
        states = list(range(1, self.win_state))
        #random.shuffle(states)
        for s in states:
            delta = max(delta, self.updateV(s))
        return delta

    def loop(self, stop_delta=.000001, stop_iterations=100000):
        ans = []
        for i in range(stop_iterations):
            delta = self.updateS()
            ans.append(delta)
            #print(f"iteration {i}, delta {delta}")
            if delta < stop_delta:
                break
        return ans

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
    d = vi.loop(stop_delta=0, stop_iterations=32)
