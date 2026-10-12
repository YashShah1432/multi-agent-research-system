# Multi-Agent Research System

An AI-powered research application built using **LangChain** and **Mistral AI** that automates the research process through multiple specialized agents. The system searches the web, extracts relevant webpage content, generates a structured research report, and evaluates the report using a Critic Agent.

## Live Demo

**[Try the Multi-Agent Research System](https://ys-multi-agent-research-system.streamlit.app/)**

## Overview

Researching a topic manually often involves searching multiple websites, reading lengthy articles, organizing information, and verifying the quality of the final report. This project simplifies that workflow by coordinating multiple AI agents, each responsible for a specific stage of the research process.

Users can enter a research topic through a Streamlit interface and receive an AI-generated report based on information retrieved from online sources.

## Features

- **Automated Web Search:** Finds relevant information using the Tavily Search API.
- **Web Scraping:** Extracts webpage text and removes unnecessary elements such as scripts, navigation bars, and footers using BeautifulSoup.
- **AI-Powered Report Generation:** Uses Mistral AI to generate a structured research report from the collected information.
- **Report Evaluation:** A Critic Agent reviews the generated report for relevance, clarity, completeness, and factual support.
- **Multi-Agent Workflow:** Coordinates specialized agents through a research pipeline.
- **Interactive UI:** Provides a Streamlit interface to submit research topics and view results.
- **Cloud Deployment:** Accessible through Streamlit Community Cloud.

## System Architecture

The project consists of four specialized agents working in sequence.

1. **Search Agent:** Searches the web for relevant information and returns titles, URLs, and snippets.
2. **Reader Agent:** Extracts URLs from the search results and scrapes relevant webpage content.
3. **Writer Agent:** Uses the collected research material to create a structured report.
4. **Critic Agent:** Evaluates the generated report and identifies areas that may need improvement.

### Workflow

User Input → Search Agent → Reader Agent → Writer Agent → Critic Agent → Research Report

## Tech Stack

- **Language:** Python
- **AI Framework:** LangChain
- **LLM:** Mistral AI
- **Web Search:** Tavily Search API
- **Web Scraping:** Requests, BeautifulSoup
- **Frontend:** Streamlit
- **Environment Management:** python-dotenv
- **Version Control:** Git and GitHub
- **Deployment:** Streamlit Community Cloud

## Project Structure

```text
multi-agent-research-system/
│
├── main.py           # Streamlit application and user interface
├── tool.py           # Web search and web scraping tools
├── agents.py         # Agent definitions and LLM prompt chains
├── pipeline.py       # Research workflow orchestration
├── requirements.txt  # Python dependencies
├── .env              # Local API keys (not committed)
├── .gitignore        # Files excluded from Git
└── README.md         # Project documentation
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd <your-repository-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Use the exact environment variable names referenced in your Python code. Never commit real API keys to GitHub.

### 5. Run the Application

```bash
streamlit run main.py
```

Open the local URL displayed in your terminal to use the application.

## Deployment

The application is deployed using Streamlit Community Cloud.

**Live application:** [https://ys-multi-agent-research-system.streamlit.app/](https://ys-multi-agent-research-system.streamlit.app/)

API credentials are configured through Streamlit's Secrets settings rather than committed to the repository.

## Future Improvements

- Add source citations and direct references to the generated report.
- Improve handling of inaccessible or unsupported webpages.
- Add report export options such as PDF and Markdown.
- Introduce iterative feedback between the Writer and Critic Agents.
- Add support for saving previous research reports.
- Improve factual verification and reduce unsupported claims.

## Disclaimer

The generated reports depend on the availability and quality of online sources and the language model's output. Always verify important claims against the original sources.

## Author

**Yash Shah**

GitHub: [YashShah1432](https://github.com/YashShah1432)
