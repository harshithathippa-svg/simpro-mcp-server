from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = FastAPI(title="Simpro MCP Server")

BASE_URL = os.getenv("SIMPRO_BASE_URL")
TOKEN = os.getenv("SIMPRO_ACCESS_TOKEN")
COMPANY_ID = os.getenv("COMPANY_ID")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def call_simpro(endpoint):
    try:
        url = f"{BASE_URL}/companies/{COMPANY_ID}/{endpoint}"

        response = requests.get(
            url,
            headers=headers
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "endpoint": endpoint
        }


@app.get("/")
def home():
    return {
        "message": "Simpro MCP Server Running Successfully",
        "base_url": BASE_URL,
        "company_id": COMPANY_ID
    }


@app.get("/mcp/customers")
def get_customers():
    return call_simpro("customers/")


@app.get("/mcp/jobs")
def get_jobs():
    return call_simpro("jobs/")


@app.get("/mcp/quotes")
def get_quotes():
    return call_simpro("quotes/")

@app.get("/tools/list")
def list_tools():
    return {
        "tools": [
            {
                "name": "customers",
                "description": "Retrieve customer records from Simpro"
            },
            {
                "name": "jobs",
                "description": "Retrieve job records from Simpro"
            },
            {
                "name": "quotes",
                "description": "Retrieve quote records from Simpro"
            }
        ]
    }

@app.post("/tools/call")
def call_tool(payload: dict):

    tool_name = payload.get("name")

    if tool_name == "customers":
        return get_customers()

    elif tool_name == "jobs":
        return get_jobs()

    elif tool_name == "quotes":
        return get_quotes()

    raise HTTPException(
        status_code=404,
        detail="Tool not found"
    )