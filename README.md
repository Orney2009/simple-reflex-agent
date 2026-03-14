# Simple Reflex Agent Demos

This workspace contains small agent demos built with LangChain and Gemini.

## Goal-based agent (modern LangChain)

File: `goal-based-agent/goal-based-demo.py`

### Requirements

- Python 3.12+
- `GOOGLE_API_KEY` set in your environment or `.env`
- Dependencies installed from `requirements.txt`

### Install

```bash
python -m pip install -r requirements.txt
```

### Run

```bash
python goal-based-agent/goal-based-demo.py
```

### Notes

- Uses modern LangChain agent API: `create_agent`
- Uses `ChatGoogleGenerativeAI` with model `gemini-2.5-flash`
- Uses thread-based in-memory conversation state with `InMemorySaver`
