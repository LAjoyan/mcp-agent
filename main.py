import asyncio
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

    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", "../mcp-server-tools", "run", "server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            server_tools = await session.list_tools()
            
            filtered_tools = [
                tool for tool in server_tools.tools 
                if "admin" not in tool.name
            ]

            print(f"Server provided {len(server_tools.tools)} tools.")
            print(f"Agent authorized for {len(filtered_tools)} tools.")

            wrapped_call = wrap_tool_call(session.call_tool)

            print("\nCalling 'get_weather' through middleware...")
            response = await wrapped_call("get_weather", {"city": "Stockholm"})
            print(response)

if __name__ == "__main__":
    asyncio.run(run_agent())