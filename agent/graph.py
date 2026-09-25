from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from agent.nodes import ai_node, analysis_node
from agent.tool_node import tool_node


def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    # If AI requested a tool, go to tool node
    if last_message.tool_calls:
        return "tools"

    # Otherwise finish
    return END

def after_tools(state: AgentState):

    last_message = state["messages"][-1]

    # If the last tool was a chart tool,
    # go directly back to the agent.
    if last_message.name and last_message.name.startswith("generate_"):
        return "agent"

    # Database result → Analysis first
    return "analysis"

graph_builder = StateGraph(AgentState)

# Add nodes
graph_builder.add_node("agent", ai_node)
graph_builder.add_node("analysis", analysis_node)
graph_builder.add_node("tools", tool_node)

# START → AI
graph_builder.add_edge(START, "agent")

# AI → Tools OR END
graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)


# Tools → AI
graph_builder.add_conditional_edges(
    "tools",
    after_tools,
    {
        "analysis": "analysis",
        "agent": "agent",
    },
)
graph_builder.add_edge("analysis", "agent")
graph_builder.add_edge("analysis", END)

# Compile
graph = graph_builder.compile()