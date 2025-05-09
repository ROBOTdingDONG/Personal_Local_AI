# backend/memory/summarizer.py
import json, datetime
import os
# import chromadb # Assuming chromadb client is needed
# from langchain_community.llms import Ollama # Example LLM import

# Placeholder content:
# 1. pull today’s messages from Chroma via metadata filter
# 2. feed them to LLM with “summarize user goals/personality changes”
# 3. merge diff into profile.json (keep version history)

PROFILE_JSON_PATH = os.path.join(os.path.dirname(__file__), 'profile.json')

print("Nightly summarizer job would run here.")

# Example structure (conceptual)
def summarize_daily_interactions():
    # chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    # collection = chroma_client.get_collection("memory")
    
    # Fetch today's messages (requires storing timestamps/metadata in Chroma)
    # today_str = datetime.date.today().isoformat()
    # # This is a conceptual filter, actual Chroma query might differ
    # # results = collection.get(where_document={"$contains": today_str}) # Example, if you stored date in docs
    # # Or if you have metadata like {'date': 'YYYY-MM-DD'}
    # # results = collection.get(where={"date": today_str})
    
    # llm = Ollama(model="llama3:70b-instruct")
    
    # # Placeholder for actual documents
    # daily_documents = ["doc1 content from today", "doc2 content from today"] 
    # if not daily_documents:
    #     print("No documents found for today.")
    #     return

    # combined_texts = "\n".join(daily_documents)
    # summary_prompt = f"Summarize the key insights, goals, and personality changes from these interactions:\n{combined_texts}"
    # summary = llm.invoke(summary_prompt)
    
    profile = {}
    if os.path.exists(PROFILE_JSON_PATH):
        try:
            with open(PROFILE_JSON_PATH, 'r') as f:
                profile = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding {PROFILE_JSON_PATH}, starting with an empty profile.")
        except FileNotFoundError:
            print(f"{PROFILE_JSON_PATH} not found, starting with an empty profile.")
            
    # Update profile (this logic needs to be robust)
    # Placeholder for summary since LLM invocation is commented out
    summary = "This is a placeholder summary. Replace with actual LLM output."
    profile.setdefault('daily_summaries', []).append({"date": datetime.date.today().isoformat(), "summary": str(summary)})
    profile['last_updated'] = datetime.datetime.now().isoformat()
    
    try:
        with open(PROFILE_JSON_PATH, 'w') as f:
            json.dump(profile, f, indent=2)
        print(f"Profile updated with summary for {datetime.date.today().isoformat()}")
    except Exception as e:
        print(f"Error writing to profile.json: {e}")

# if __name__ == "__main__":
#    print(f"Attempting to run summarizer. Profile path: {PROFILE_JSON_PATH}")
#    # summarize_daily_interactions() # This would require Ollama and Chroma to be running and configured
#    print("Summarizer finished (conceptual run).")
