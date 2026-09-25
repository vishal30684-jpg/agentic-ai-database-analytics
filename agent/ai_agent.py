import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage
load_dotenv()


async def main():

    # Connect to MCP MySQL server
    client = MultiServerMCPClient(
        {
            "mysql": {
                "command": "python",
                "args": ["mcp_servers/mysql_server.py"],
                "transport": "stdio",
            }
        }
    )

    # Get MCP tools
    tools = await client.get_tools()

    print("\nMCP Tools:\n")

    for tool in tools:
        print("-", tool.name)

    # Create OpenAI model
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Give tools to the model
    model_with_tools = model.bind_tools(tools)

    # User question
    question = "How many customers are in the database?"

    print("\nUser Question:")
    print(question)

    # First AI call
    response = await model_with_tools.ainvoke(question)

    print("\nAI Tool Call:")
    print(response.tool_calls)

    # Execute the requested MCP tool
    if response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print("\nExecuting MCP Tool:")
        print(tool_name)

        print("\nSQL:")
        print(tool_args["query"])

        # Find the MCP tool
        selected_tool = next(
            tool for tool in tools
            if tool.name == tool_name
        )

        # Execute MCP tool
        tool_result = await selected_tool.ainvoke(tool_args)

        print("\nMySQL Result:")
        print(tool_result)

        # Send result back to OpenAI
        tool_message = ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"]
        )
        final_response = await model.ainvoke(
            [
               ("user", question),
                response,
                tool_message,
            ]
       )

        print("\nFinal AI Answer:")
        print(final_response.content)

    else:

        print("\nAI Answer:")
        print(response.content)


if __name__ == "__main__":
    asyncio.run(main())