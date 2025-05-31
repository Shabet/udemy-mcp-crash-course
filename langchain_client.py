import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI()

async def main():
    print("Starting langchain mcp")
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "/Users/pjy/work/udemy-mcp-crash-course/servers/math_server.py"
                ],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    #result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
    result = await agent.ainvoke({"messages": [HumanMessage(content="What is the weather in San Francisco? use the weather tool.")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
