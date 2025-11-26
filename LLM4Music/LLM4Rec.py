import requests
import os, socket
print("Host:", socket.gethostname())
print("CWD:", os.getcwd())

SYSTEM = """You are the master music recommender system.
For example:
Example1: 

Example2: 

Example3: 
"""

def query_ollama_chat(model, prompt_question, max_token = 2048):
    payload = {
        "model": model,
        "stream": False,
        "options": {"temperature": 0,
                    "num_gpu": 1, #change to cpu, I think it can run on your local desk
                    "max_tokens": max_token},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt_question}
        ]
    }
    r = requests.post("http://localhost:11434/api/chat", json=payload, timeout=None)
    r.raise_for_status()
    data = r.json()
    return (data.get("message") or {}).get("content","").strip()

with open("input file", encoding="utf-8") as f, open("output results","w",encoding="utf-8") as w:
    for line in f:
        t = line.strip() + "Output format: a python list. Do not explain the reason or include any other words"

        g = query_ollama_chat('gemma3:4b',t)
        w.write(f"{g}\n")
        print(f"{t} => {g}")

