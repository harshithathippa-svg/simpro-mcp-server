from pathlib import Path
import sys
import json

# ---------------- ROOT PATH ----------------
ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import mcp_server
simpro_tools = mcp_server.simpro_tools

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    chat_id: str
    message: str
    provider: str = "openai"
    messages: list = []

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"status": "API running"}

# ---------------- CHAT ----------------
@app.post("/chat")
def chat(req: ChatRequest):

    msg = req.message.lower().strip()
    print("MESSAGE RECEIVED:", msg)

    try:

        # ---------------- JOBS ----------------
        if msg == "jobs":
            result = simpro_tools["jobs"]()
            return {
                "chat_id": req.chat_id,
                "reply": json.dumps(result, indent=2),
                "provider": req.provider
            }

        # ---------------- CUSTOMERS ----------------
        if msg == "customers":
            result = simpro_tools["customers"]()
            return {
                "chat_id": req.chat_id,
                "reply": json.dumps(result, indent=2),
                "provider": req.provider
            }

        # ---------------- QUOTES ----------------
        if msg == "quotes":
            result = simpro_tools["quotes"]()
            return {
                "chat_id": req.chat_id,
                "reply": json.dumps(result, indent=2),
                "provider": req.provider
            }

        # ---------------- JOB DETAILS ----------------
        if msg.startswith("job "):
            job_id = msg.split()[1]
            result = simpro_tools["get_job"](job_id)
            return {
                "chat_id": req.chat_id,
                "reply": json.dumps(result, indent=2),
                "provider": req.provider
            }

        # ---------------- SECTIONS ----------------
        if msg.startswith("sections "):
            job_id = msg.split()[1]
            result = simpro_tools["get_job_sections"](job_id)
            return {
                "chat_id": req.chat_id,
                "reply": json.dumps(result, indent=2),
                "provider": req.provider
            }

        # ---------------- SECTION DETAILS ----------------
        if msg.startswith("section "):
            parts = msg.split()
            result = simpro_tools["get_section"](parts[1], parts[2])
            return {
                "chat_id": req.chat_id,
                "reply": json.dumps(result, indent=2),
                "provider": req.provider
            }

        # ---------------- COST CENTERS ----------------
        if msg.startswith("costcenters "):
            parts = msg.split()

            job_id = parts[1]
            section_id = parts[2]

            result = simpro_tools["get_cost_centers"](job_id, section_id)

            return {
                "chat_id": req.chat_id,
                "reply": json.dumps(result, indent=2),
                "provider": req.provider
            }

        # ---------------- DEFAULT ----------------
        return {
            "chat_id": req.chat_id,
            "reply": f"FASTAPI RECEIVED: {req.message}",
            "provider": req.provider
        }

    except Exception as e:
        return {
            "chat_id": req.chat_id,
            "reply": json.dumps({"error": str(e)}),
            "provider": req.provider
        }