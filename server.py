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
                   body: dict[str, Any] | None = None) -> str:
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(method, url, headers=_headers(),
                                      params=params, json=body if body else None)
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
    """Create a new user."""
    return await _request("POST", "/user", body=body)

@tool(description="Creates list of users with given input array [WRITES DATA]")
async def createuserswitharrayinput(body: list) -> str:
    """Create users from array."""
    return await _request("POST", "/user/createWithArray", body=body)

@tool(description="Creates list of users with given input array [WRITES DATA]")
async def createuserswithlistinput(body: list) -> str:
    """Create users from list."""
    return await _request("POST", "/user/createWithList", body=body)

@tool(description="Returns pet inventories by status")
async def getinventory() -> str:
    """Get inventory status."""
    return await _request("GET", "/store/inventory")

@tool(description="Search or list pet with flexible filtering.")
async def search_pet(status: str | None = None, tags: str | None = None, petId: str | None = None) -> str:
    """Search pets by status, tags, or ID."""
    if petId:
        return await _request("GET", f"/pet/{petId}")
    params = {}
    if status:
        return await _request("GET", "/pet/findByStatus", params={"status": status})
    if tags:
        return await _request("GET", "/pet/findByTags", params={"tags": tags})
    return json.dumps({"error": "Must provide status, tags, or petId"})

@tool(description="Search or list user with flexible filtering.")
async def search_user(username: str | None = None, password: str | None = None) -> str:
    """Search users by username or login/logout."""
    if username:
        return await _request("GET", f"/user/{username}")
    if password:
        return await _request("GET", "/user/login", params={"username": username, "password": password})
    return await _request("GET", "/user/logout")

@tool(description="Update an existing pet [WRITES DATA]")
async def updatepet(body: dict) -> str:
    """Update pet details."""
    return await _request("PUT", "/pet", body=body)

@tool(description="Updates a pet in the store with form data [WRITES DATA]")
async def updatepetwithform(petId: str, name: str | None = None, status: str | None = None) -> str:
    """Update pet with form data."""
    body = {}
    if name:
        body["name"] = name
    if status:
        body["status"] = status
    return await _request("POST", f"/pet/{petId}", body=body)

@tool(description="Updated user [WRITES DATA]")
async def updateuser(username: str, body: dict) -> str:
    """Update user details."""
    return await _request("PUT", f"/user/{username}", body=body)

@tool(description="uploads an image [WRITES DATA]")
async def uploadfile(petId: str, additionalMetadata: str | None = None, file: str | None = None) -> str:
    """Upload pet image."""
    body = {}
    if additionalMetadata:
        body["additionalMetadata"] = additionalMetadata
    if file:
        body["file"] = file
    return await _request("POST", f"/pet/{petId}/uploadImage", body=body)

server = MCPServer("swagger-petstore")
server.collect(
    addpet,
    createuser,
    createuserswitharrayinput,
    createuserswithlistinput,
    getinventory,
    search_pet,
    search_user,
    updatepet,
    updatepetwithform,
    updateuser,
    uploadfile
)
if __name__ == "__main__":
    asyncio.run(server.serve())