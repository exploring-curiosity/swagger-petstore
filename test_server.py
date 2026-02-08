import asyncio
import json
from typing import Any
from dedalus_mcp.client import MCPClient
import pytest

async def test_list_tools():
    """Verify exactly 11 tools are registered."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        assert len(tools) == 11, f"Expected 11 tools, got {len(tools)}"

async def test_tool_schemas():
    """Each tool has name + description."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        for tool in tools:
            assert "name" in tool, f"Tool missing name: {tool}"
            assert "description" in tool, f"Tool missing description: {tool}"

async def test_addpet():
    """Call tool 'addpet' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("addpet", {
            "name": "Fluffy",
            "photoUrls": ["http://example.com/fluffy.jpg"],
            "status": "available"
        })
        assert isinstance(result, str)

async def test_createuser():
    """Call tool 'createuser' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuser", {
            "username": "testuser",
            "email": "user@example.com"
        })
        assert isinstance(result, str)

async def test_createuserswitharrayinput():
    """Call tool 'createuserswitharrayinput' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswitharrayinput", {
            "users": [{"username": "user1"}, {"username": "user2"}]
        })
        assert isinstance(result, str)

async def test_createuserswithlistinput():
    """Call tool 'createuserswithlistinput' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("createuserswithlistinput", {
            "users": [{"username": "user3"}, {"username": "user4"}]
        })
        assert isinstance(result, str)

async def test_getinventory():
    """Call tool 'getinventory' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("getinventory", {})
        assert isinstance(result, str)

async def test_search_pet():
    """Call tool 'search_pet' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("search_pet", {
            "status": "available",
            "limit": 5
        })
        assert isinstance(result, str)

async def test_search_user():
    """Call tool 'search_user' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("search_user", {
            "username": "test",
            "limit": 10
        })
        assert isinstance(result, str)

async def test_updatepet():
    """Call tool 'updatepet' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("updatepet", {
            "id": 1,
            "name": "Updated Name",
            "status": "pending"
        })
        assert isinstance(result, str)

async def test_updatepetwithform():
    """Call tool 'updatepetwithform' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("updatepetwithform", {
            "petId": 1,
            "name": "New Name",
            "status": "sold"
        })
        assert isinstance(result, str)

async def test_updateuser():
    """Call tool 'updateuser' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("updateuser", {
            "username": "testuser",
            "email": "new@example.com"
        })
        assert isinstance(result, str)

async def test_uploadfile():
    """Call tool 'uploadfile' with sample args."""
    async with await MCPClient.connect("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("uploadfile", {
            "petId": 1,
            "file": "test.jpg"
        })
        assert isinstance(result, str)

async def main():
    """Run all test functions."""
    tests = [
        test_list_tools(),
        test_tool_schemas(),
        test_addpet(),
        test_createuser(),
        test_createuserswitharrayinput(),
        test_createuserswithlistinput(),
        test_getinventory(),
        test_search_pet(),
        test_search_user(),
        test_updatepet(),
        test_updatepetwithform(),
        test_updateuser(),
        test_uploadfile()
    ]
    for test in tests:
        try:
            await test
            print(f"PASSED: {test.__name__}")
        except Exception as e:
            print(f"FAILED: {test.__name__} - {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())