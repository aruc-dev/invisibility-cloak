
import os, subprocess, json, requests

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def run_ollama(prompt: str, model: str = None):
    model = model or OLLAMA_MODEL
    try:
        res = subprocess.run(["ollama", "run", model],
                             input=prompt.encode("utf-8"),
                             capture_output=True, timeout=90)
        out = (res.stdout or b"").decode("utf-8", "ignore")
        return out.strip() or "[empty]"
    except Exception as e:
        return f"[Ollama error] {e}"

def run_openai(prompt: str, model: str = None):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[OpenAI fallback disabled]"
    try:
        import requests
        model = model or OPENAI_MODEL
        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers={"Authorization": f"Bearer {api_key}"},
                          json={"model": model,
                                "messages":[{"role":"user","content": prompt}],
                                "temperature":0})
        r.raise_for_status()
        j = r.json()
        return j["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenAI error] {e}"

def smart_llm(prompt: str):
    out = run_ollama(prompt)
    if out.lower().startswith("[ollama error]") or out.strip() == "[empty]":
        return run_openai(prompt)
    return out
