# LangGraph_AI-Agents-WebSearch-QA

A multi-agent research assistant pipeline built with [LangGraph](https://www.langgraph.dev/) and [Streamlit](https://streamlit.io/). This project automates technical question answering by breaking the task into specialized agents:

1. **Query Builder** – formulates 3–5 search queries from user input
2. **Searcher** – uses the Tavily API to retrieve information
3. **Synthesizer** – condenses retrieved content
4. **Final Writer** – composes a concise, cited technical answer

---

## 🚀 Features
- Multi-agent orchestration via LangGraph
- Technical synthesis from real-time web search
- Customizable prompt logic
- Interactive Streamlit UI

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/fabriciocarraro/LangGraph_AI-Agents-WebSearch-QA.git
cd LangGraph_AI-Agents-WebSearch-QA

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Setup API Keys

1. Create a `.env` file based on the provided `.env.example`:

```bash
cp .env.example .env
```

2. Add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. Add your Tavily API key:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## 🧪 Usage

Run the Streamlit app:

```bash
streamlit run graph.py
```

Enter a technical question in the input box, click **Search**, and watch the multi-agent pipeline generate a detailed response with references.

---

## 🙌 Acknowledgments
- [LangGraph](https://www.langgraph.dev/)
- [Tavily](https://www.tavily.com/)
- [Streamlit](https://streamlit.io/)

