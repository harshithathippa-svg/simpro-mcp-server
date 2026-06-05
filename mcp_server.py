from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = os.getenv("SIMPRO_BASE_URL")
TOKEN = os.getenv("SIMPRO_ACCESS_TOKEN")
COMPANY_ID = os.getenv("COMPANY_ID")


headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

mcp = FastMCP("Simpro MCP")


def call_simpro(endpoint):
    try:
        url = f"{BASE_URL}/v1.0/companies/{COMPANY_ID}/{endpoint}"

        print("Calling URL:", url)

        response = requests.get(
            url,
            headers=headers
        )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "endpoint": endpoint
        }



@mcp.tool()
def customers():
    return call_simpro("customers")

@mcp.tool()
def jobs():
    return call_simpro("jobs")


@mcp.tool()
def quotes():
    return call_simpro("quotes")

@mcp.tool()
def get_cost_center(
    job_id: int,
    section_id: int,
    cost_center_id: int
):
    endpoint = (
        f"jobs/{job_id}/sections/"
        f"{section_id}/costCenters/{cost_center_id}"
    )

    return call_simpro(endpoint)


if __name__ == "__main__":
    print("Simpro MCP Server Started")
    mcp.run()