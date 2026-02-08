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
            assert "name" in tool, f"Tool missing 'name': {tool}"
            assert "description" in tool, f"Tool missing 'description': {tool}"

async def test_addpet():
    """Call tool 'addpet' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("addpet", {
            "name": "Fluffy",
            "photoUrls": ["http://example.com/fluffy.jpg"],
            "status": "available"
        })
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        try:
            json.loads(result)  # Verify it's valid JSON
        except json.JSONDecodeError:
            assert False, "Result is not valid JSON"

async def test_createuser():
    """Call tool 'createuser' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuser", {
            "username": "testuser",
            "email": "user@example.com"
        })
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Result is not valid JSON"

async def test_createuserswitharrayinput():
    """Call tool 'createuserswitharrayinput' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswitharrayinput", {
            "users": [
                {"username": "user1", "email": "user1@example.com"},
                {"username": "user2", "email": "user2@example.com"}
            ]
        })
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Result is not valid JSON"

async def test_createuserswithlistinput():
    """Call tool 'createuserswithlistinput' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswithlistinput", {
            "users": [
                {"username": "user3", "email": "user3@example.com"},
                {"username": "user4", "email": "user4@example.com"}
            ]
        })
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Result is not valid JSON"

async def test_search_pet():
    """Call tool 'search_pet' with sample args and verify it returns a string."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("search_pet", {
            "status": "available",
            "limit": 5
        })
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        try:
            json.loads(result)
        except json.JSONDecodeError:
            assert False, "Result is not valid JSON"

async def main():
    """Run all test functions."""
    tests = [
        test_list_tools,
        test_tool_schemas,
        test_addpet,
        test_createuser,
        test_createuserswitharrayinput,
        test_createuserswithlistinput,
        test_search_pet
    ]
    
    for test in tests:
        try:
            await test()
            print(f"PASSED: {test.__name__}")
        except AssertionError as e:
            print(f"FAILED: {test.__name__} - {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())