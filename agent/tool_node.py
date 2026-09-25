from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage
from agent.state import AgentState


async def tool_node(state: AgentState):

    # Connect to MCP MySQL server
    client = MultiServerMCPClient(
        {
           "local_mysql": {
            "command": "python",
            "args": ["mcp_servers/mysql_server.py"],
            "transport": "stdio",
        },

        "remote_mysql": {
            "url": "http://127.0.0.1:8001/mcp",
            "transport": "streamable_http",
            },
        "chart_mcp": { "url": "http://127.0.0.1:1122/mcp", "transport": "streamable_http", }
        }
    )

    # Get MCP tools
    tools = await client.get_tools()

    # Get the latest AI message
    last_message = state["messages"][-1]

    results = []

    # Execute every tool call requested by AI
    for tool_call in last_message.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Find requested MCP tool
        selected_tool = next(
            tool for tool in tools
            if tool.name == tool_name
        )

        # Execute tool
        tool_result = await selected_tool.ainvoke(tool_args)
        print("\n--- MCP TOOL CALL ---")
        print("Tool:", tool_name)
        print("Arguments:", tool_args)
        print("Tool Result:", tool_result)
        print("---------------------")

        results.append(
            ToolMessage(
              content=str(tool_result),
              tool_call_id=tool_call["id"],
              name=tool_name,
            )
      )

    return {
        "messages": results
    }