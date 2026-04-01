import random

class QLearningAgent:
    def __init__(self, actions=4, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.05):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.actions = actions

    def get_key(self, state):
        return tuple(state)

    def choose_action(self, state):
        key = self.get_key(state)

        if key not in self.q_table:
            self.q_table[key] = [0]*self.actions

        # exploration vs exploitation
        if random.random() < self.epsilon:
            return random.randint(0, self.actions-1)

        return self.q_table[key].index(max(self.q_table[key]))

    def update(self, state, action, reward, next_state):
        key = self.get_key(state)
        next_key = self.get_key(next_state)

        if next_key not in self.q_table:
            self.q_table[next_key] = [0]*self.actions

        old = self.q_table[key][action]
        next_max = max(self.q_table[next_key])

        self.q_table[key][action] = old + self.alpha * (reward + self.gamma * next_max - old)

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay