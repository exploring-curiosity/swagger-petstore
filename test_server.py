import asyncio
import json
from typing import Any
import pytest
from dedalus_mcp.client import MCPClient

async def test_list_tools():
    """Verify exactly 4 tools are registered."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        assert len(tools) == 4, f"Expected 4 tools, got {len(tools)}"

async def test_tool_schemas():
    """Each tool has name + description."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        for tool in tools:
            assert "name" in tool, f"Tool missing name: {tool}"
            assert "description" in tool, f"Tool missing description: {tool}"

async def test_addpet():
    """Call tool 'addpet' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("addpet", {
            "name": "doggie",
            "photoUrls": ["http://example.com/photo.jpg"],
            "status": "available"
        })
        assert isinstance(result, str), f"Expected string response, got {type(result)}"
        # Verify response can be parsed as JSON
        json.loads(result)

async def test_createuser():
    """Call tool 'createuser' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuser", {
            "username": "testuser",
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com"
        })
        assert isinstance(result, str), f"Expected string response, got {type(result)}"
        json.loads(result)

async def test_createuserswitharrayinput():
    """Call tool 'createuserswitharrayinput' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswitharrayinput", {
            "users": [
                {
                    "username": "user1",
                    "firstName": "User",
                    "lastName": "One",
                    "email": "user1@example.com"
                },
                {
                    "username": "user2",
                    "firstName": "User",
                    "lastName": "Two",
                    "email": "user2@example.com"
                }
            ]
        })
        assert isinstance(result, str), f"Expected string response, got {type(result)}"
        json.loads(result)

async def test_createuserswithlistinput():
    """Call tool 'createuserswithlistinput' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswithlistinput", {
            "users": [
                {
                    "username": "user3",
                    "firstName": "User",
                    "lastName": "Three",
                    "email": "user3@example.com"
                },
                {
                    "username": "user4",
                    "firstName": "User",
                    "lastName": "Four",
                    "email": "user4@example.com"
                }
            ]
        })
        assert isinstance(result, str), f"Expected string response, got {type(result)}"
        json.loads(result)

async def main():
    """Run all tests."""
    await test_list_tools()
    await test_tool_schemas()
    await test_addpet()
    await test_createuser()
    await test_createuserswitharrayinput()
    await test_createuserswithlistinput()
    print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())