from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from pathlib import Path
import requests
import os

# ---------------- LOAD ENV (FIXED ABSOLUTE PATH) ----------------
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

print("Loading .env from:", ENV_PATH)
load_dotenv(dotenv_path=ENV_PATH)

BASE_URL = os.getenv("SIMPRO_BASE_URL")
TOKEN = os.getenv("SIMPRO_ACCESS_TOKEN")
COMPANY_ID = os.getenv("COMPANY_ID")

print("BASE_URL:", BASE_URL)
print("COMPANY_ID:", COMPANY_ID)

# ---------------- VALIDATION (IMPORTANT) ----------------
if not BASE_URL:
    raise Exception("❌ SIMPRO_BASE_URL not loaded. Check .env location")

if not COMPANY_ID:
    raise Exception("❌ COMPANY_ID not loaded. Check .env file")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

mcp = FastMCP("Simpro MCP")

# ---------------- CORE API CALL ----------------
def call_simpro(endpoint):
    try:
        url = f"{BASE_URL}/v1.0/companies/{COMPANY_ID}/{endpoint}/"

        print("CALLING:", url)

        res = requests.get(url, headers=headers, timeout=30)

        print("STATUS:", res.status_code)

        if res.status_code != 200:
            return {
                "error": "API failed",
                "status": res.status_code,
                "body": res.text
            }

        return res.json()

    except Exception as e:
        return {"error": str(e)}

# ---------------- TOOLS ----------------
@mcp.tool()
def jobs():
    return call_simpro("jobs")

@mcp.tool()
def customers():
    return call_simpro("customers")

@mcp.tool()
def quotes():
    return call_simpro("quotes")

@mcp.tool()
def get_job(job_id: int):
    return call_simpro(f"jobs/{job_id}")

@mcp.tool()
def get_job_sections(job_id: int):
    return call_simpro(f"jobs/{job_id}/sections")

@mcp.tool()
def get_section(job_id: int, section_id: int):
    return call_simpro(f"jobs/{job_id}/sections/{section_id}")

@mcp.tool()
def get_cost_centers(job_id: int, section_id: int):
    return call_simpro(f"jobs/{job_id}/sections/{section_id}/costCenters")

@mcp.tool()
def get_cost_center(job_id: int, section_id: int, cost_center_id: int):
    return call_simpro(
        f"jobs/{job_id}/sections/{section_id}/costCenters/{cost_center_id}"
    )

# ---------------- EXPORT ----------------
simpro_tools = {
    "jobs": jobs,
    "customers": customers,
    "quotes": quotes,
    "get_job": get_job,
    "get_job_sections": get_job_sections,
    "get_section": get_section,
    "get_cost_centers": get_cost_centers,
    "get_cost_center": get_cost_center,
}

# ---------------- TEST ----------------
if __name__ == "__main__":
    print(jobs())