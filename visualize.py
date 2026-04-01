def render(env):
    size = env.size
    grid = [["." for _ in range(size)] for _ in range(size)]

    ax, ay = env.agent
    gx, gy = env.goal

    grid[gx][gy] = "🏁"
    grid[ax][ay] = "🤖"

    for ox, oy in env.obstacles:
        grid[ox][oy] = "❌"

    print("\n".join([" ".join(row) for row in grid]))
    print("=" * 25)