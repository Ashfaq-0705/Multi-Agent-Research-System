# ResearchMind

ResearchMind is a Streamlit app that uses a multi-agent workflow to research a topic and produce a downloadable report. Its agents search the web, read a selected source, draft a report, and review the result.

## Features

- Search for recent information with Tavily.
- Scrape and extract text from a selected web page.
- Generate a structured report with OpenRouter's `openai/gpt-4o-mini` model.
- Review the report with a critic chain.
- View the pipeline progress and download the report as Markdown.

## Requirements

- Python 3.10 or later
- An [OpenRouter API key](https://openrouter.ai/keys)
- A [Tavily API key](https://app.tavily.com/)

## Setup

Clone the repository and enter its folder:

```powershell
git clone https://github.com/Ashfaq-0705/Multi-Agent-Research-System.git
Set-Location Multi-Agent-Research-System
```

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your local environment file and add your API keys:

```powershell
Copy-Item .env.example .env
```

Edit `.env`:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep `.env` private; it is excluded from Git.

## Run

From the project folder, start the Streamlit app:

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit (usually <http://localhost:8501>), enter a research topic, and select **Research**. When the pipeline completes, the report and critic feedback appear on the page. Use **Download Report** to save the report as a Markdown file.

## Pipeline

1. **Search** — finds recent web results with Tavily.
2. **Read** — scrapes a relevant page for additional detail.
3. **Write** — drafts a structured research report.
4. **Review** — evaluates the report and provides feedback.

The app makes requests to OpenRouter and Tavily, so valid API keys and internet access are required to run a research job.
