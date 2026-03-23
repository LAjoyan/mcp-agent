import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from functools import wraps

def wrap_tool_call(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        
        processed_content = f"--- PROCESSED BY AGENT MIDDLEWARE ---\n{result.content[0].text}\n------------------------------------"
        return processed_content
    return wrapper

async def run_agent():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_dir = os.path.join(base_dir, "mcp-server-tools")
    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", server_dir, "run", "server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            server_tools = await session.list_tools()
            
            authorized_names = [
                tool.name for tool in server_tools.tools 
                if "admin" not in tool.name
            ]

            print(f"Server provided {len(server_tools.tools)} tools.")
            print(f"Agent authorized for {len(authorized_names)} tools.")

            tool_to_call = "get_weather"

            if tool_to_call not in authorized_names:
                print(f"\n❌ SECURITY ALERT: Access Denied! '{tool_to_call}' is restricted.")
            else:
                wrapped_call = wrap_tool_call(session.call_tool)
                print(f"\nCalling '{tool_to_call}' through middleware...")
                
                args = {"city": "Stockholm"} if tool_to_call == "get_weather" else {}
                response = await wrapped_call(tool_to_call, args)
                print(response)

if __name__ == "__main__":
    asyncio.run(run_agent())