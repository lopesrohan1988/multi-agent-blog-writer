# app/agents/planner.py (Corrected)

from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
# The import below is no longer needed
# from langgraph.prebuilt.tool_executor import ToolExecutor 
from langchain_core.tools import tool

# You can reuse the tools from our shared tools file
from app.agents.tools import web_search_tool

# Import AgentState from its new location
from app.graph_state import AgentState

# Define the Planner agent's prompt
planner_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert planner for a content creation team. Your job is to take a user's request for a blog post and create a detailed outline. Your outline must be clear, actionable, and ready for a researcher to follow. Be very specific."),
    ("human", "{topic}")
])

# The agent's function
def planner_node(state: AgentState):
    """This node defines the Planner agent's behavior."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5)
    
    # We are not giving the planner any tools, as its job is just to think
    planner_agent = planner_prompt | llm
    
    # Get the user's topic from the state
    topic = state['messages'][-1].content
    
    # Generate the plan
    plan_message = planner_agent.invoke({"topic": topic})
    
    # Store the plan in the state and pass it to the next agent
    return {"messages": [plan_message], "plan": plan_message.content, "topic": topic, "intermediate_steps": []}