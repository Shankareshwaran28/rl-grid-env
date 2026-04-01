from env import GridEnv

def get_tasks():
    return {
        "easy": GridEnv(4),
        "medium": GridEnv(6),
        "hard": GridEnv(8)
    }