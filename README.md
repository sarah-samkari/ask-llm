# ask-llm

A small command-line tool that takes a question, sends it to Google's Gemini
API, and prints back clean, validated JSON — parsed into a Pydantic model
rather than trusted blindly.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Get a free API key from [Google AI Studio](https://aistudio.google.com), then set it as an environment variable:

```bash
$env:GEMINI_API_KEY="your-key-here"     # PowerShell
```

## Usage

You can also pick a different model with `--model`, e.g. `python -m ask_llm.cli "..." --model gemini-3.6-flash`.

```bash
python -m ask_llm.cli "What is the capital of France?"
```

Example output:

```json
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "confidence": 1.0,
  "reasoning": "Paris is universally recognized as the capital of France.",
  "sources": ["Geographical knowledge base"]
}
```

## How it works

- `ask_llm/models.py` — defines the `Answer` Pydantic model (the expected shape of the response)
- `ask_llm/client.py` — calls the Gemini API, handles network/HTTP/JSON errors, validates the result against `Answer`
- `ask_llm/cli.py` — the command-line entry point