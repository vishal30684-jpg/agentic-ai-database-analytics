# Agentic AI Database Analytics Platform

An AI-powered database analytics platform that uses LangGraph, MCP, MySQL, FastAPI, and an interactive web interface to query, analyze, compare, and visualize data from multiple databases.

## 🚀 Features

* 🤖 Agentic AI workflow using LangGraph
* 🔌 MCP-based database tool integration
* 🗄️ Local MySQL database support
* 🌐 Remote MySQL database support
* 🔄 Compare data across multiple databases
* 🧠 Analysis node for processing database results
* 📊 Automatic chart generation using Chart MCP
* 💬 Persistent chat history
* 🧠 Long-term user memory
* 🔒 Read-only SQL safety checks
* ⚡ FastAPI backend
* 🌐 Web-based chat interface
* 🟢 Real-time server Online/Offline status

## 🏗️ Architecture

```text
User
  ↓
Web Frontend
  ↓
FastAPI
  ↓
LangGraph Agent
  ↓
MCP Tools
  ├── Local MySQL MCP
  ├── Remote MySQL MCP
  └── Chart MCP
  ↓
Analysis Node
  ↓
Final Agent
  ↓
Answer + Visualization
```

## 🛠️ Technologies

* Python
* LangGraph
* MCP / FastMCP
* LangChain
* OpenAI
* MySQL
* FastAPI
* JavaScript
* HTML
* CSS
* Chart MCP

## 📁 Project Structure

```text
agentic-ai-db/
│
├── agent/
│   ├── graph.py
│   ├── nodes.py
│   ├── state.py
│   ├── tool_node.py
│   ├── run_agent.py
│   └── ai_agent.py
│
├── backend/
│   └── main.py
│
├── database/
│   └── schema.sql
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── mcp_servers/
│   ├── mysql_server.py
│   └── remote_mysql_server.py
│
├── mcp_client.py
├── .gitignore
└── README.md
```

## 🔐 Security

Database credentials are stored in environment variables and are not committed to GitHub.

The MCP database tools implement read-only SQL restrictions and reject multiple SQL statements.

## ▶️ Running the Project

### 1. Activate virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Start the Remote MySQL MCP Server

```powershell
python mcp_servers\remote_mysql_server.py
```

### 3. Start Chart MCP

```powershell
mcp-server-chart --transport streamable --host 127.0.0.1 --port 1122
```

### 4. Start FastAPI

```powershell
uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 💡 Example Questions

```text
How many customers are in the local database?
```

```text
How many customers are in the remote database?
```

```text
Compare the total sales of the local and remote databases.
```

```text
Compare the total sales of the local and remote databases and show me a bar chart.
```

## 🎯 Project Goal

The goal of this project is to build an agentic AI system capable of interacting with databases through MCP, reasoning over retrieved data, comparing multiple data sources, and presenting analytical results and visualizations through a web interface.

## 👨‍💻 Author

Vishal Panwar
