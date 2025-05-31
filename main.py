import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_ollama import ChatOllama
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(model="llama3.2")

stdio_server_params = StdioServerParameters(
    command="python",
    args=["/Users/pjy/work/udemy-mcp-crash-course/servers/math_server.py"],
)

async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)
            print(f"tools: {tools}")

            agent = create_react_agent(llm, tools)
            
            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3 ?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
