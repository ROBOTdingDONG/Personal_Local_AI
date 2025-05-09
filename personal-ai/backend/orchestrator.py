# backend/orchestrator.py
from langchain_ollama import OllamaLLM, OllamaEmbeddings # Updated import
from langgraph.graph import StateGraph
# from langgraph.memory import VectorMemory # This specific class might need verification for its API
from chromadb import HttpClient
from langchain_community.vectorstores import Chroma
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
import os

# LLM & embeddings
llm = OllamaLLM(model="llama3:70b-instruct") # Updated class
emb = OllamaEmbeddings(model="llama3:8b-embed") # Updated class

# Chroma-backed memory
chroma_client = HttpClient(host="localhost", port=8000)

# Ensure the memory directory exists for profile.json
# Construct path relative to this script file for profile.json
# __file__ is the path to the current script. os.path.dirname(__file__) is its directory.
# os.path.join constructs a path like backend/memory/profile.json
PROFILE_JSON_PATH = os.path.join(os.path.dirname(__file__), 'memory', 'profile.json')

# Initialize vector store
vector_store = Chroma(client=chroma_client, collection_name="memory", embedding_function=emb)

def retrieve_memories(user_msg, k=5):
    return vector_store.similarity_search(user_msg, k=k)

def store_memory(text):
    vector_store.add_texts([text])

# LangGraph State definition
class AgentState(TypedDict):
    input: str
    answer: str
    # history: Annotated[list, add_messages] # If chat history management is needed directly in state

# Node that retrieves memories → composes prompt → calls LLM
def respond(state: AgentState):
    user_msg = state["input"]
    retrieved_docs = retrieve_memories(user_msg, k=5)
    memories_text = "\n".join([doc.page_content for doc in retrieved_docs])
    
    profile_content = "{}" # Default empty JSON
    if os.path.exists(PROFILE_JSON_PATH):
        try:
            with open(PROFILE_JSON_PATH, 'r') as f:
                profile_content = f.read()
        except Exception as e:
            print(f"Error reading profile.json: {e}")
            # Keep profile_content as "{}"
    else:
        print(f"Profile.json not found at {PROFILE_JSON_PATH}, using default.")

    prompt = f"""You are Mr. Powell’s lifelong advisor.
### Known profile
{profile_content}
### Relevant past facts
{memories_text}
### New user input
{user_msg}
### Helpful reply
"""
    answer = llm.invoke(prompt)
    store_memory(user_msg + "\n" + str(answer)) # Ensure answer is string
    return {"answer": str(answer)} # Ensure answer is string

g = StateGraph(AgentState)
g.add_node("respond", respond)
g.set_entry_point("respond")
g.set_finish_point("respond") 

agent = g.compile()

def chat_with_memory(msg: str):
    result_state = agent.invoke({"input": msg})
    return result_state.get("answer"), None
