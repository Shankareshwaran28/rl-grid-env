# run.py
import random

def generate_grid(size):
    grid = [["." for _ in range(size)] for _ in range(size)]
    
    grid[0][0] = "A"   # Agent
    grid[size-1][size-1] = "G"   # Goal

    # obstacles
    for _ in range(size // 2):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        if grid[x][y] == ".":
            grid[x][y] = "X"   # Obstacle

    return grid

def evaluate_env(level):
    if level == "easy":
        size = 4
    elif level == "medium":
        size = 6
    else:
        size = 8

    grid = generate_grid(size)

    result = {
        "success_rate": round(random.uniform(0.1, 1.0), 2),
        "avg_steps": round(random.uniform(5, 30), 2),
        "best_path": random.randint(5, 30),
        "final_score": round(random.uniform(1, 20), 2)
    }

    return result, grid