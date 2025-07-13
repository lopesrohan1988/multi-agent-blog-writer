# app/graph.py (Corrected conditional edge)

from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from app.graph_state import AgentState
from app.agents.planner import planner_node
from app.agents.researcher import researcher_node
from app.agents.writer import writer_node
from app.agents.tools import web_search_tool
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, BaseMessage, AIMessage, ToolMessage

# Define the tools the tool node can execute
tools = [web_search_tool]
tool_node = ToolNode(tools)

# Define the graph
def create_graph():
    workflow = StateGraph(AgentState)

    # Add the Planner and Researcher decision nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)

    # Add the ToolNode which will execute tools
    workflow.add_node("tool", tool_node)
    workflow.add_node("writer", writer_node)
    # Define the entry point
    workflow.set_entry_point("planner")

    # The Planner always goes to the Researcher
    workflow.add_edge("planner", "researcher")

    # Conditional edge from researcher: tool if tool_calls, else writer
    workflow.add_conditional_edges(
        "researcher",
        lambda state: "tool" if isinstance(state["messages"][-1], AIMessage) and state["messages"][-1].tool_calls else "writer", # <--- Changed END to writer
        {
            "tool": "tool",
            "writer": "writer" # <--- Route to writer if no tool calls
        }
    )

    # The Tool Node always goes back to the Researcher (for the next decision)
    workflow.add_edge("tool", "researcher")
    

    # After the writer is done, the graph ends
    workflow.add_edge("writer", END) #
    
    # Compile the graph
    app = workflow.compile()
    return app