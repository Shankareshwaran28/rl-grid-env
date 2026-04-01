from agent import QLearningAgent

def train_and_evaluate(env, episodes=500):
    agent = QLearningAgent()
    success = 0
    total_steps = 0
    best_path = float("inf")

    progress = []

    for ep in range(episodes):
        state = env.reset()
        steps = 0

        for _ in range(60):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)

            agent.update(state, action, reward, next_state)

            state = next_state
            steps += 1
            total_steps += 1

            if done:
                if state == env.goal:
                    success += 1
                    best_path = min(best_path, steps)
                break

        agent.decay_epsilon()

        # track progress every 50 episodes
        if (ep + 1) % 50 == 0:
            progress.append(success / (ep + 1))

    success_rate = success / episodes
    avg_steps = total_steps / episodes

    score = (success_rate * 70) + (1 / (best_path + 1) * 30)

    return {
        "success_rate": round(success_rate, 2),
        "avg_steps": round(avg_steps, 2),
        "best_path": best_path if best_path != float("inf") else -1,
        "final_score": round(score, 2),
        "learning_progress": progress
    }