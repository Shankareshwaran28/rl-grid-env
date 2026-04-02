import random

class GridEnv:
    def __init__(self, level="easy"):
        self.level = level
        self.size = {"easy": 4, "medium": 6, "hard": 8}.get(level, 4)
        self.agent_pos = [0, 0]
        self.goal_pos = [self.size - 1, self.size - 1]
        self.obstacles = self._generate_obstacles()
        self.steps = 0
        self.max_steps = self.size * self.size * 2

    def _generate_obstacles(self):
        obstacles = []
        for _ in range(self.size // 2):
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if [x, y] not in ([0, 0], self.goal_pos):
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
        dx, dy = {0:(-1,0), 1:(1,0), 2:(0,-1), 3:(0,1)}.get(action, (0,0))
        nx, ny = x+dx, y+dy
        if 0 <= nx < self.size and 0 <= ny < self.size and [nx,ny] not in self.obstacles:
            self.agent_pos = [nx, ny]
        if self.agent_pos == self.goal_pos:
            return self._get_obs(), 10.0, True, {"result": "success", "steps": self.steps}
        if self.steps >= self.max_steps:
            return self._get_obs(), -1.0, True, {"result": "timeout", "steps": self.steps}
        return self._get_obs(), -0.1, False, {"steps": self.steps}

    def _get_obs(self):
        return {"agent": self.agent_pos, "goal": self.goal_pos, "obstacles": self.obstacles, "size": self.size}

    def get_grid(self):
        grid = [["." for _ in range(self.size)] for _ in range(self.size)]
        for o in self.obstacles:
            grid[o[0]][o[1]] = "X"
        grid[self.goal_pos[0]][self.goal_pos[1]] = "G"
        grid[self.agent_pos[0]][self.agent_pos[1]] = "A"
        return grid


def evaluate_env(level="easy", episodes=20):
    env = GridEnv(level=level)
    success_count = 0
    total_steps = 0
    best_steps = None
    best_path = []

    for _ in range(episodes):
        obs = env.reset()
        done = False
        steps = 0
        path = [env.agent_pos.copy()]

        while not done:
            action = random.choice([0, 1, 2, 3])
            obs, reward, done, info = env.step(action)
            steps += 1
            path.append(env.agent_pos.copy())

            if done:
                if info.get("result") == "success":
                    success_count += 1
                    if best_steps is None or steps < best_steps:
                        best_steps = steps
                        best_path = path.copy()
                total_steps += steps
                break

    avg_steps = total_steps / episodes if episodes > 0 else 0
    success_rate = success_count / episodes if episodes > 0 else 0
    final_score = success_rate * 100 - (avg_steps * 0.5)
    final_score = max(final_score, 0)

    return {
        "success_rate": f"{success_rate*100:.1f}%",
        "avg_steps": f"{avg_steps:.1f}",
        "best_path": str(best_path),
        "final_score": round(final_score, 2)
    }, env.get_grid()