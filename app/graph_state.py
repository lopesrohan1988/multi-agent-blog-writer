from typing import Annotated, List, TypedDict, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """The state for our multi-agent workflow."""
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    plan: str
    research_results: str
    blog_draft: str 
    topic: str
    intermediate_steps: Annotated[List[Any], lambda x, y: x + y]