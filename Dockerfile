FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "inference.py"]
```

Click **Commit changes** ✅

---

### Step 3 — Edit `requirements.txt` directly on HF

Go to: **https://huggingface.co/spaces/Shankareshwaran28/rl-grid-env/edit/main/requirements.txt**

Replace with:
```
fastapi
uvicorn
pydantic
matplotlib
numpy