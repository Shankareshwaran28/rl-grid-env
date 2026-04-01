import random

class GridEnv:
    def __init__(self, size=5):
        self.size = size
        self.reset()

    def reset(self):
        self.agent = [0, 0]
        self.goal = [self.size - 1, self.size - 1]
        self.obstacles = self._generate_obstacles()
        return self.agent

    def _generate_obstacles(self):
        obs = set()
        while len(obs) < 3:
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if pos != (0,0) and pos != tuple(self.goal):
                obs.add(pos)
        return [list(p) for p in obs]

    def step(self, action):
        x, y = self.agent

        if action == 0: x -= 1
        elif action == 1: x += 1
        elif action == 2: y -= 1
        elif action == 3: y += 1

        x = max(0, min(self.size-1, x))
        y = max(0, min(self.size-1, y))

        self.agent = [x, y]

        reward = -1
        done = False

        if self.agent in self.obstacles:
            return self.agent, -10, True

        if self.agent == self.goal:
            return self.agent, 25, True

        return self.agent, reward, done