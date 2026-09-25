from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    analysis: str | None