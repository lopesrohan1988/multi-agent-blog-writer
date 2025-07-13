from langgraph.graph import StateGraph, END
from app.agents.planner import planner_node, AgentState
from app.agents.tools import web_search_tool, ToolExecutor

# Define a tool executor for our agent to use.
tools = [web_search_tool]
tool_executor = ToolExecutor(tools)

# Define the graph
def create_graph():
    workflow = StateGraph(AgentState)

    # Add the Planner node to the graph
    workflow.add_node("planner", planner_node)

    # Set the entry point of the graph
    workflow.set_entry_point("planner")

    # For now, we just end the graph after the planner is done
    workflow.add_edge("planner", END)

    # Compile the graph
    app = workflow.compile()
    return app