# 🤖 Multi-Agent Research System

An AI-powered research assistant built using **LangChain**, **Google Gemini**, **Tavily Search**, and **Streamlit**. The system uses multiple AI agents to search the web, extract information, generate a structured research report, and critique its own output.

---

## 🚀 Features

- 🔍 **Web Search Agent**
  - Searches the web for recent and reliable information using Tavily.

- 📖 **Reader Agent**
  - Selects the most relevant webpage and extracts useful content.

- ✍️ **Writer Agent**
  - Generates a detailed research report based on collected information.

- 🧐 **Critic Agent**
  - Reviews the generated report and provides feedback with strengths, weaknesses, and suggestions.

- 🌐 **Interactive Streamlit UI**
  - Simple interface for entering a research topic and viewing AI-generated reports.

---

## 🏗️ Project Architecture

```
                User
                  │
                  ▼
         Streamlit Interface
                  │
                  ▼
        Research Pipeline
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
 Search Agent  Reader Agent  Writer Chain
     │            │            │
     ▼            ▼            ▼
 Tavily API   Web Scraping   Research Report
                  │
                  ▼
            Critic Chain
                  │
                  ▼
            Final Output
```

---

## 🛠️ Tech Stack

- Python 3.13
- Streamlit
- LangChain
- Google Gemini 2.5 Flash
- Tavily Search API
- BeautifulSoup4
- Requests
- Python Dotenv

---

## 📂 Project Structure

```
MULTI_AGENT_SYSTEM/
│
├── app.py                 # Streamlit Application
├── pipeline.py            # Research Pipeline
├── agents.py              # Search & Reader Agents
├── tools.py               # Search & Web Scraping Tools
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/vaibhav0076/YOUR_REPOSITORY_NAME.git
```

Move into the project

```bash
cd YOUR_REPOSITORY_NAME
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### Home Page

> Add a screenshot here

### Generated Report

> Add another screenshot here

---

## 🔄 Workflow

1. User enters a research topic.
2. Search Agent searches the web.
3. Reader Agent extracts detailed webpage content.
4. Writer Agent generates a research report.
5. Critic Agent reviews the report.
6. Final report and feedback are displayed.

---

## 🎯 Future Improvements

- Multiple source summarization
- PDF export
- Citation generation
- Report revision loop
- Memory using LangGraph
- RAG integration
- Research history
- Multi-source comparison
- Better web scraping using Playwright or Firecrawl

---

## 👨‍💻 Author

**Vaibhav Kumar Raghuvanshi**

GitHub: https://github.com/vaibhav0076

LinkedIn: *(Add your LinkedIn profile here)*

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.