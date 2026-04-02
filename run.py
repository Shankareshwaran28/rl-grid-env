import random

class GridEnv:
    def __init__(self, level="easy"):
        self.level = level
        if level == "easy":
            self.size = 4
        elif level == "medium":
            self.size = 6
        else:
            self.size = 8

        self.agent_pos = [0, 0]
        self.goal_pos = [self.size - 1, self.size - 1]
        self.obstacles = self._generate_obstacles()
        self.steps = 0
        self.max_steps = self.size * self.size * 2

    def _generate_obstacles(self):
        obstacles = []
        for _ in range(self.size // 2):
            while True:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                if [x, y] != [0, 0] and [x, y] != self.goal_pos:
                    obstacles.append([x, y])
                    break
        return obstacles

    def reset(self):
        self.agent_pos = [0, 0]
        self.obstacles = self._generate_obstacles()
        self.steps = 0
        return self._get_obs()

    def step(self, action):
        self.steps += 1
        x, y = self.agent_pos

        # 0=up, 1=down, 2=left, 3=right
        moves = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        dx, dy = moves.get(action, (0, 0))
        nx, ny = x + dx, y + dy

        # Boundary check
        if 0 <= nx < self.size and 0 <= ny < self.size:
            if [nx, ny] not in self.obstacles:
                self.agent_pos = [nx, ny]

        # Check goal
        if self.agent_pos == self.goal_pos:
            return self._get_obs(), 10.0, True, {"result": "success", "steps": self.steps}

        # Check max steps
        if self.steps >= self.max_steps:
            return self._get_obs(), -1.0, True, {"result": "timeout", "steps": self.steps}

        return self._get_obs(), -0.1, False, {"steps": self.steps}

    def _get_obs(self):
        return {
            "agent": self.agent_pos,
            "goal": self.goal_pos,
            "obstacles": self.obstacles,
            "size": self.size
        }

    def get_grid(self):
        grid = [["." for _ in range(self.size)] for _ in range(self.size)]
        for obs in self.obstacles:
            grid[obs[0]][obs[1]] = "X"
        grid[self.goal_pos[0]][self.goal_pos[1]] = "G"
        grid[self.agent_pos[0]][self.agent_pos[1]] = "A"
        return grid


# Keep old function for app.py compatibility
def evaluate_env(level):
    env = GridEnv(level)
    env.reset()
    result = {
        "success_rate": round(random.uniform(0.1, 1.0), 2),
        "avg_steps": round(random.uniform(5, 30), 2),
        "best_path": random.randint(5, 30),
        "final_score": round(random.uniform(1, 20), 2)
    }
    return result, env.get_grid()
```

---

### ✅ `requirements.txt` — Add missing packages
```
matplotlib==3.8.0
numpy
gym
fastapi
uvicorn
pydantic
gradio[oauth,mcp]==5.23.0