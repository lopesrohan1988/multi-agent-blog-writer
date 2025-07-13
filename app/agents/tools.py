import os
from langchain_core.tools import tool, Tool
from langchain_google_community import GoogleSearchAPIWrapper
from typing import Annotated, Any


# Create the Google Search API wrapper, passing the CSE ID
google_search = GoogleSearchAPIWrapper(google_cse_id=os.environ.get("GOOGLE_CSE_ID"))

# Create a LangChain Tool from the wrapper
web_search_tool = Tool(
    name="Google_Search",
    description="Search Google for recent results.",
    func=google_search.run,
)

# A simple tool for the Critic to use to check if the writing is good
@tool
def quality_check(draft: Annotated[str, "The draft of the blog post to be checked."]) -> str:
    """A tool that checks the overall quality, tone, and grammar of a blog post draft."""
    if len(draft) < 200:
        return "Draft is too short. Please write more content."
    if "spelling" in draft.lower() or "grammar" in draft.lower():
        return "The draft needs a thorough grammar and spell check."
    return "The draft looks good and is ready for final review."

# A placeholder tool to simulate getting feedback from the Critic
@tool
def get_feedback(draft: Annotated[str, "The draft of the blog post to get feedback on."]) -> str:
    """A tool that retrieves feedback on a draft from another agent or an internal system."""
    return "Feedback: The introduction is good, but the third paragraph needs more detail from the research."