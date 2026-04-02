from app import iface  # your app.py contains the Gradio app
from fastapi.responses import JSONResponse

# Add /reset endpoint
app = iface.app

@app.post("/reset")
async def reset():
    return JSONResponse({"status": "ok"})

# launch the Gradio interface
iface.launch(server_name="0.0.0.0", server_port=7860)