# SQL Query Agent

An interactive Python CLI that uses a Groq-powered LangChain SQL agent to answer natural-language questions against a SQLite database.

## Features

- Auto-creates a demo e-commerce database when `demo.sqlite` is missing
- Runs in read-only mode by default
- Supports interactive chat or one-off questions from the command line

## Requirements

- Python 3.10+
- A Groq API key

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `example.env` to `.env` and fill in your API key:
   ```bash
   copy example.env .env
   ```

3. Run the agent:
   ```bash
   python app.py
   ```

## Usage

Ask a question interactively:

```bash
python app.py
```

Ask a single question:

```bash
python app.py --question "Which customer spent the most?"
```

Use a different database:

```bash
python app.py --db path\\to\\your.db
```

Allow write access:

```bash
python app.py --allow-write
```

## Environment

The app reads environment variables from `.env`.

Required:

- `GROQ_API_KEY`

