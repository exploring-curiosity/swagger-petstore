import asyncio
import json
from typing import Any
import pytest
from dedalus_mcp.client import MCPClient

async def test_list_tools():
    """Verify exactly 5 tools are registered."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        assert len(tools) == 5, f"Expected 5 tools, got {len(tools)}"

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
            "photoUrls": ["http://example.com/photo.jpg"]
        })
        assert isinstance(result, str)
        try:
            json.loads(result)  # Verify it's valid JSON
        except json.JSONDecodeError:
            assert False, "Response is not valid JSON"

async def test_createuser():
    """Call tool 'createuser' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuser", {
            "username": "testuser",
            "email": "user@example.com"
        })
        assert isinstance(result, str)
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Response is not valid JSON"

async def test_createuserswitharrayinput():
    """Call tool 'createuserswitharrayinput' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswitharrayinput", {
            "users": [{"username": "user1"}, {"username": "user2"}]
        })
        assert isinstance(result, str)
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Response is not valid JSON"

async def test_createuserswithlistinput():
    """Call tool 'createuserswithlistinput' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswithlistinput", {
            "users": [{"username": "user3"}, {"username": "user4"}]
        })
        assert isinstance(result, str)
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Response is not valid JSON"

async def test_getinventory():
    """Call tool 'getinventory' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("getinventory", {})
        assert isinstance(result, str)
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Response is not valid JSON"

async def main():
    """Run all test functions."""
    await test_list_tools()
    await test_tool_schemas()
    await test_addpet()
    await test_createuser()
    await test_createuserswitharrayinput()
    await test_createuserswithlistinput()
    await test_getinventory()
    print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())