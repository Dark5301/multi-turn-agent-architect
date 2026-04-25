# 💬 Multi-Turn AI Agent Architect — Conversational Agent Design with Instructor + Groq

A Python project that enables **multi-turn, conversational agent blueprint generation** using Groq's `llama-3.3-70b-versatile` and schema-enforced structured outputs via [Instructor](https://python.useinstructor.com/) and Pydantic.

Unlike a single-shot prompt, this script maintains full conversation history — meaning you can **refine, follow up, and iterate** on agent ideas across multiple turns in the same session, and the model remembers everything you've discussed.

---

## 📌 What It Does

You have an ongoing conversation with a Senior AI Agent Architect persona. Each turn, your message and the model's structured response are appended to a shared history list, giving the LLM full context of the conversation so far.

This enables patterns like:
- *"Design a scholarship research agent"* → get a full blueprint
- *"Now make it specifically for postgraduate students applying abroad"* → refined blueprint with prior context intact
- *"What if we added a document upload feature?"* → iterative update without starting over

Every response is validated against the same strict `Assistant` Pydantic schema, so all outputs remain structured and consistent across the entire session.

---

## 🧱 Output Schema

Each response is validated against the `Assistant` model:

| Field                  | Type              | Constraints                         |
|------------------------|-------------------|-------------------------------------|
| `agent_name`           | `str`             | 5–50 characters                     |
| `short_description`    | `str`             | 100–1500 characters                 |
| `target_users`         | `list[str]`       | 3–5 specific personas               |
| `core_tools_needed`    | `list[str]`       | 4–6 specific functions/integrations |
| `suggested_tech_stack` | `list[str]`       | 4–7 Python-based tools              |
| `first_milestone`      | `str`             | 100–500 characters, 14-day target   |
| `potential_challenges` | `list[str]`       | 3–5 technical or logical risks      |
| `confidence`           | `Confidence` enum | `"high"`, `"medium"`, or `"low"`    |

---

## 🔑 Key Concept: Conversation History

The core pattern that makes this multi-turn is the `user_history` list passed into every call:

```python
def ask_structured_question(user_string: str, user_history: list):
    user_history.append({'role': 'user', 'content': user_string})
    messages = [{'role': 'system', 'content': system_prompt}] + user_history
    data = client.create(...)
    user_history.append({'role': 'assistant', 'content': data.model_dump_json()})
```

Each assistant response is serialised back to JSON via `model_dump_json()` and appended to history, so the model receives its own prior structured outputs as context on subsequent turns.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Groq](https://groq.com/) | Fast LLM inference (LLaMA 3.3 70B) |
| [Instructor](https://python.useinstructor.com/) | Structured output enforcement via Pydantic |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation and schema definition |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Secure API key management |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dark5301/multi-turn-agent-architect.git
cd multi-turn-agent-architect
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install groq instructor pydantic python-dotenv
```

### 4. Set up your environment variables

Create a `.env` file in the root of the project:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com).

### 5. Run the script

```bash
python multi_turn_agent.py
```

You'll be dropped into an interactive prompt. Type your agent idea and press Enter. Type `exit` to end the session.

---

## 📤 Example Session

```
Ask your question (Type "exit" to exit)
> Design a research agent for Indian students finding scholarships

Agent Name: ScholarPath AI
Short description: ScholarPath AI autonomously scans scholarship databases, filters
opportunities by eligibility, and assists with essay drafting...
Target users:
. First-generation college students in Tier-2/Tier-3 cities
. Postgraduate students seeking international funding
. Students from low-income households unfamiliar with government schemes
...
Confidence: high

Ask your question (Type "exit" to exit)
> Refine it to focus only on students applying to UK universities

Agent Name: ScholarPath UK
Short description: ScholarPath UK narrows its search to UK-specific funding sources
like Chevening, Commonwealth, and university scholarships, with tailored essay
guidance aligned to UCAS and institutional requirements...
...
Confidence: high

Ask your question (Type "exit" to exit)
> exit
```

---

## ⚠️ Known Limitations

- **No session persistence**: Conversation history exists only in memory for the duration of the script run. Exiting the session clears all history.
- **Context window growth**: Each turn appends both the user message and the full serialised assistant response to history. Long sessions can approach the model's context window limit.
- **Instructor + Groq schema strictness**: Groq enforces strict JSON schema validation on tool calls. Complex `Union` types in Pydantic models can cause validation errors. The `max_retries=3` setting mitigates transient failures. For production multi-turn agentic workflows, consider migrating to [PydanticAI](https://ai.pydantic.dev), which handles conversation history and tool-calling natively.

---

## 🔮 Roadmap

- [ ] Migrate to [PydanticAI](https://ai.pydantic.dev) for native multi-turn and tool-calling support
- [ ] Persist conversation history to a `.json` file between sessions
- [ ] Add a `--resume` flag to reload a previous session
- [ ] Export final agent blueprint to a structured `.md` or `.json` file
- [ ] Add token usage tracking to warn before context window is exceeded

---

## 👤 Author

**Prince**
Aspiring AI/Cybersecurity Developer · Python · Bash · JavaScript
Building a portfolio at the intersection of AI agents and penetration testing.

---

## 📄 License

MIT License — feel free to fork, modify, and build on this.
