import os

from dotenv import load_dotenv
load_dotenv()


from langchain_core.messages import HumanMessage
from app.graph import create_graph


# Create and compile the graph
app = create_graph()

# Define the starting input
topic = "Write a blog post about the benefits of modular smart home systems."
initial_state = {"messages": [HumanMessage(content=topic)], "topic": topic, "intermediate_steps": [], "plan": "", "research_results": "", "blog_draft": ""}

print(f"Starting workflow for topic: {topic}\n")

# Run the graph in a single invocation to get the final state
final_state = app.invoke(initial_state)

print("--- Final Blog Post Draft ---")
if final_state and "blog_draft" in final_state:
    print(final_state["blog_draft"])
else:
    print("No blog draft generated.")