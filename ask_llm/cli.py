import argparse
import os
import sys

from .client import DEFAULT_MODEL, LLMError, ask_llm


def main():
    parser = argparse.ArgumentParser(description="Ask an LLM a question, get back validated JSON.")
    parser.add_argument("question", help="The question to ask.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL}).")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: set the GEMINI_API_KEY environment variable first.", file=sys.stderr)
        sys.exit(2)

    try:
        answer = ask_llm(args.question, api_key=api_key, model=args.model)
    except LLMError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(answer.json(indent=2))


if __name__ == "__main__":
    main()