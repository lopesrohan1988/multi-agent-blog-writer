from typing import Annotated, List, TypedDict, Any
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# Import AgentState from its new location
from app.graph_state import AgentState
from app.agents.tools import web_search_tool

# This agent will need its own prompt
researcher_prompt = hub.pull("hwchase17/openai-tools-agent")

# The agent's function
def researcher_node(state: AgentState):
    """This node defines the Researcher agent's behavior."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5)
    
    # We will give this agent the web search tool
    research_agent = create_tool_calling_agent(llm, [web_search_tool], researcher_prompt)
    
    # The agent needs a specific input format
    agent_input = {
        "input": state["plan"],
        "intermediate_steps": state["intermediate_steps"],
    }

    action = research_agent.invoke(agent_input)

    return {"messages": [action]}