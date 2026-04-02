RUN --mount=target=/tmp/requirements.txt,source=requirements.txt \
    pip install --no-cache-dir -r /tmp/requirements.txt \
    gradio[oauth,mcp]==6.10.0 \
    "uvicorn>=0.14.0" \
    "websockets>=10.4" \
    spaces>=0.48.1