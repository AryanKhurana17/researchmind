# ResearchMind - Local AI Research Agent

ResearchMind is an autonomous, multi-agent AI research pipeline powered by LangChain and local LLMs (Ollama + Mistral). It takes any topic and orchestrates a collaborative workflow between four specialized agents to search the web, scrape deep content, synthesize findings, and review the final output to produce a highly detailed, comprehensive research report.

## Features

- **100% Local Inference**: Runs locally via Ollama (Mistral) to ensure privacy and eliminate API token costs.
- **Multi-Agent Pipeline**:
  - **Search Agent**: Queries the web for recent and relevant sources (powered by Tavily API).
  - **Reader Agent**: Scrapes and extracts deep text content from the top URLs, bypassing noise.
  - **Writer Agent**: Synthesizes the gathered intelligence into a structured, comprehensive, and factual 1500+ word report.
  - **Critic Agent**: Reviews the drafted report for quality, bias, and completeness.
- **Premium Streamlit UI**: A sleek, dark-themed UI with animated gradients, step-by-step progress tracking, and interactive example chips.
- **Rich Output**: The final report includes an Executive Summary, In-Depth Analysis, Stakeholder Perspectives, Strategic Scenarios, Mitigation Strategies, and a complete list of sources.
- **Exportable**: One-click download of the generated report in Markdown format.

## Tech Stack

- **Framework**: LangChain, LangGraph
- **LLM**: Ollama (Mistral 7B)
- **Search API**: Tavily
- **Frontend**: Streamlit
- **Web Scraping**: BeautifulSoup4, Requests

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AryanKhurana17/researchmind.git
   cd researchmind
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Tavily API key:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

5. **Install and Run Ollama:**
   - Download and install [Ollama](https://ollama.com/).
   - Pull the Mistral model:
     ```bash
     ollama run mistral
     ```

## Running the App

Start the Streamlit application:

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`. Enter a research topic in the input field or click one of the example chips to launch the multi-agent pipeline.

## Project Structure

- `app.py`: The Streamlit frontend, containing the sleek UI and the session state logic to progressively execute the pipeline.
- `pipeline.py`: A CLI-based entry point to run the multi-agent orchestration without the UI.
- `agents.py`: Defines the prompts, chains, and agent instantiations for the Search, Reader, Writer, and Critic modules.
- `tools.py`: Contains the custom LangChain tools (`web_search` and `scrape_url`) utilized by the agents.

## License

This project is licensed under the MIT License.
