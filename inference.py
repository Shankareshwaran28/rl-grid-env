from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from run import GridEnv

app = FastAPI()

# Global environment instance
env = GridEnv(level="easy")
current_state = None

class StepRequest(BaseModel):
    action: int  # 0=up, 1=down, 2=left, 3=right

class ResetRequest(BaseModel):
    level: str = "easy"

@app.post("/reset")
async def reset(req: ResetRequest = None):
    global env, current_state
    level = req.level if req else "easy"
    env = GridEnv(level=level)
    current_state = env.reset()
    return JSONResponse({
        "observation": current_state,
        "info": {"level": level, "grid_size": env.size}
    })

@app.post("/step")
async def step(req: StepRequest):
    global current_state
    obs, reward, done, info = env.step(req.action)
    current_state = obs
    return JSONResponse({
        "observation": obs,
        "reward": reward,
        "terminated": done,
        "truncated": False,
        "info": info
    })

@app.get("/state")
async def state():
    return JSONResponse({
        "observation": current_state,
        "grid": env.get_grid()
    })

@app.get("/info")
async def info():
    return JSONResponse({
        "name": "SmartRL-Grid",
        "description": "RL Grid Environment with agent, goal, and obstacles",
        "actions": {"0": "up", "1": "down", "2": "left", "3": "right"},
        "observation_space": "grid positions",
        "reward_range": [-1, 10]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)