from typing import Annotated, List, TypedDict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Import AgentState from our shared state file
from app.graph_state import AgentState

# Define the Writer agent's prompt
# This prompt guides the LLM to act as a blog post writer
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert blog post writer. Your task is to write a comprehensive and engaging blog post based on the provided outline (plan) and research results.
    
    Follow the plan strictly for structure.
    Integrate the research results naturally into the relevant sections.
    Ensure the tone is informative and engaging.
    The blog post should be well-structured with an introduction, body paragraphs (following the plan's sections), and a conclusion.
    
    Plan:
    {plan}
    
    Research Results:
    {research_results}
    """),
    ("human", "Please write the blog post now.")
])

# The agent's function
def writer_node(state: AgentState):
    """This node defines the Writer agent's behavior."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5)
    
    # Create the writer agent runnable
    writer_agent = writer_prompt | llm
    
    # Get the plan and research results from the state
    plan = state["plan"]
    research_results = state["research_results"] # This will be populated by the Researcher
    
    # Generate the blog post draft
    blog_draft_message = writer_agent.invoke({"plan": plan, "research_results": research_results})
    
    # Store the generated draft in the state
    return {"messages": [blog_draft_message], "blog_draft": blog_draft_message.content}