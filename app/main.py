import os
import getpass
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from app.graph import create_graph

# Load environment variables
load_dotenv()

# Set up API keys from .env or via user input
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Enter API key for Tavily: ")

# Create and compile the graph
app = create_graph()

# Define the starting input
topic = "The rise of generative AI in education."
initial_state = {"messages": [HumanMessage(content=topic)], "topic": topic}

# Run the graph and print the output
for state in app.stream(initial_state):
    print(state)