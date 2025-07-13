from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from typing import Annotated, Any

# A web search tool that our agents can use
web_search_tool = TavilySearchResults()

# A simple tool for the Critic to use to check if the writing is good
@tool
def quality_check(draft: Annotated[str, "The draft of the blog post to be checked."]) -> str:
    """A tool that checks the overall quality, tone, and grammar of a blog post draft."""
    # In a real-world scenario, this could be a more complex LLM call
    # or a rule-based system. For now, it's a simple placeholder.
    if len(draft) < 200:
        return "Draft is too short. Please write more content."
    if "spelling" in draft.lower() or "grammar" in draft.lower():
        return "The draft needs a thorough grammar and spell check."
    return "The draft looks good and is ready for final review."

# A placeholder tool to simulate getting feedback from the Critic
@tool
def get_feedback(draft: Annotated[str, "The draft of the blog post to get feedback on."]) -> str:
    """A tool that retrieves feedback on a draft from another agent or an internal system."""
    # This is a placeholder for the Critic's actual output.
    return "Feedback: The introduction is good, but the third paragraph needs more detail from the research."