# Foundry Fabric Agent Chat UI

A Streamlit-based chat application that connects to an Azure AI Foundry Agent with Fabric Data Agent integration using user authentication (Entra ID).

---

## 🚀 Features

- ✅ Interactive **chat UI (Streamlit)**
- ✅ **User authentication** via Entra ID (InteractiveBrowserCredential)
- ✅ **Session-based chat memory** using Foundry `conversation_id`
- ✅ **"New Chat" support** (starts a fresh conversation)
- ✅ **Fabric Data Agent integration** for data-driven answers
- ✅ Clean, minimal chat output (no tool noise)

---

## 🧠 Architecture

User (Streamlit Chat UI)
│
├── Session State
│     ├── auth (cached login)
│     ├── conversation_id
│     └── chat_history
│
▼
Azure AI Foundry Agent (/responses)
│
▼
Fabric Data Agent (tool)


📁 Project Structure
foundry-fabric-agent-chat/
│
├── app/
│   ├── __init__.py
│   ├── chat_ui.py         # Streamlit chat UI (entry point)
│   ├── config.py          # Loads environment variables
│   ├── auth.py            # Entra ID authentication (user login)
│   ├── foundry_client.py  # Calls Foundry Agent (/responses)
│
├── .env                   # Local configuration (NOT committed)
├── requirements.txt       # Python dependencies
├── README.md



## ⚙️ Prerequisites

- Python 3.10+
- Azure subscription
- Azure AI Foundry project with:
  - published agent
  - Fabric Data Agent tool configured
- Entra ID access to the agent

---

## 🔐 Configuration

Create a `.env` file:


TENANT_ID=<your-tenant-id>

FOUNDRY_RESPONSES_URL=https://<your-foundry-endpoint>/responses?api-version=v1
FOUNDRY_ACTIVITY_URL=https://<your-foundry-endpoint>/activityprotocol?api-version=v1

🧪 Run Locally (Streamlit UI)
1. Create and activate virtual environment
Shellpython -m venv .venv# Windows.venv\Scripts\activate# macOS/Linuxsource .venv/bin/activateShow more lines

2. Install dependencies
Shellpip install -r requirements.txtShow more lines

3. Run the chat UI
Shellstreamlit run app/chat_ui.pyShow more lines

4. Open browser
http://localhost:8501


💬 How it Works
✅ First message

No conversation_id sent
Foundry creates a conversation

✅ Subsequent messages

App reuses returned conversation_id
Context is preserved

✅ New Chat button

Clears conversation_id
Starts a fresh session


📊 Observability (Important)

Each user message = new traceId in Foundry
Conversations are still maintained internally via conversation_id
Multiple traceIds per chat session = ✅ expected behavior

⚠️ Notes

Do NOT manually generate conversation_id
Always use the one returned by Foundry
.env is excluded from Git via .gitignore (for security)