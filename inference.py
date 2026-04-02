from app import iface
from fastapi.responses import JSONResponse

# ✅ Must call queue() or load app BEFORE accessing .app
iface.queue()

# ✅ Add /reset POST endpoint
app = iface.app

@app.post("/reset")
async def reset():
    return JSONResponse({"status": "ok"})

# ✅ Single launch point
iface.launch(server_name="0.0.0.0", server_port=7860)