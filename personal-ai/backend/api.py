# backend/api.py
from flask import Flask, request, jsonify
from orchestrator import chat_with_memory

app = Flask(__name__)

@app.post("/api/chat")
def chat():
    user_msg = request.json["message"]
    resp, sources = chat_with_memory(user_msg)
    return jsonify({"answer": resp, "citations": sources})

if __name__ == "__main__":
    app.run(port=5050)
