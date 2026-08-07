# PDF Q&A Agent

A simple Python CLI app that reads a PDF file and lets you ask questions about it using LlamaIndex and Groq.

## Features
- Build a vector index from a local PDF
- Ask questions interactively in the terminal
- Ask a single question directly from the command line

## Requirements
- Python 3.10+
- A Groq API key

## Setup
1. Install the dependencies:
   ```bash
   pip install -r requirement.txt
   ```
2. Create a `.env` file in this folder and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Example:
   ```env
   GROQ_API_KEY=ghp_1234567890abcdef1234567890abcdef
   ```
3. Run the app:
   ```bash
   python app.py --pdf path/to/your.pdf
   ```

## Usage

### Interactive mode
Ask questions one by one:
```bash
python app.py --pdf path/to/your.pdf
```

### Single-question mode
Ask one question directly:
```bash
python app.py --pdf path/to/your.pdf --query "What is this document about?"
```

## Example input
You can provide the PDF path and the question as input like this:
```bash
python app.py --pdf docs/sample.pdf --query "Summarize the main points of this document."
```

To exit the interactive prompt, type `quit` or `exit`.
