from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from typing import TypedDict, List, Annotated

class State(TypedDict):
    messages : Annotated[List[AnyMessage],add_messages]
    tool_required:bool = False
    card : str | None