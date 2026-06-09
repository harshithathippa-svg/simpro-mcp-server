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
        url = f"{BASE_URL}/v1.0/companies/{COMPANY_ID}/{endpoint}/"

        print("\nCalling URL:", url)

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


def test_info():
    url = f"{BASE_URL}/v1.0/info/"

    print("\nCalling:", url)

    response = requests.get(
        url,
        headers=headers
    )

    print("Status:", response.status_code)
    print(response.text)


def test_companies():
    url = f"{BASE_URL}/v1.0/companies/"

    print("\nCalling:", url)

    response = requests.get(
        url,
        headers=headers
    )

    print("Status:", response.status_code)
    print(response.text)

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
def get_job(job_id: int):
    return call_simpro(
        f"jobs/{job_id}"
    )


@mcp.tool()
def get_job_sections(job_id: int):
    return call_simpro(
        f"jobs/{job_id}/sections"
    )


@mcp.tool()
def get_section(
    job_id: int,
    section_id: int
):

    return call_simpro(
        f"jobs/{job_id}/sections/{section_id}"
    )


@mcp.tool()
def get_cost_centers(
    job_id: int,
    section_id: int
):

    return call_simpro(
        f"jobs/{job_id}/sections/{section_id}/costCenters"
    )


@mcp.tool()
def get_cost_center(
    job_id: int,
    section_id: int,
    cost_center_id: int
):

    return call_simpro(
        f"jobs/{job_id}/sections/{section_id}/costCenters/{cost_center_id}"
    )



if __name__ == "__main__":
    print("Simpro MCP Server Started")

    mcp.run()