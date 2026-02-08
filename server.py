from __future__ import annotations
import asyncio, json, os
from typing import Any
import httpx
from dedalus_mcp import MCPServer, tool

BASE_URL = os.getenv("SWAGGER_PETSTORE_BASE_URL", "https://petstore.swagger.io/v2")
API_KEY = os.getenv("SWAGGER_PETSTORE_API_KEY", "")

def _headers() -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if API_KEY:
        headers["api_key"] = API_KEY
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers

async def _request(method: str, path: str, *, params: dict[str, Any] | None = None,
                   body: dict[str, Any] | list[Any] | None = None) -> str:
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(
                method,
                url,
                headers=_headers(),
                params=params,
                json=body if body else None
            )
            resp.raise_for_status()
            try:
                return json.dumps(resp.json(), indent=2)
            except Exception:
                return resp.text
        except httpx.HTTPStatusError as e:
            return json.dumps({"error": str(e), "status": e.response.status_code})
        except Exception as e:
            return json.dumps({"error": str(e)})

@tool(description="Add a new pet to the store [WRITES DATA]")
async def addpet(body: dict) -> str:
    """Add a new pet to the store."""
    return await _request("POST", "/pet", body=body)

@tool(description="Create user [WRITES DATA]")
async def createuser(body: dict) -> str:
    """Create user."""
    return await _request("POST", "/user", body=body)

@tool(description="Creates list of users with given input array [WRITES DATA]")
async def createuserswitharrayinput(body: list) -> str:
    """Creates list of users with given input array."""
    return await _request("POST", "/user/createWithArray", body=body)

@tool(description="Creates list of users with given input array [WRITES DATA]")
async def createuserswithlistinput(body: list) -> str:
    """Creates list of users with given input array."""
    return await _request("POST", "/user/createWithList", body=body)

server = MCPServer("swagger-petstore")
server.collect(addpet, createuser, createuserswitharrayinput, createuserswithlistinput)
if __name__ == "__main__":
    asyncio.run(server.serve())