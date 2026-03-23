# MCP Agent Orchestrator

This project acts as an AI Agent client that connects to an external MCP Server, filters available tools, and processes all outputs using a middleware wrapper.

## 🛠 Features & Requirements
- **Automatic Connection**: Connects to the `mcp-server-tools` repository using `StdioServerParameters`.
- **Tool Filtering**: Upon initialization, the agent fetches 5 tools but programmatically filters out any tool containing "admin" in its name.
- **Output Middleware**: Uses a `@wrap_tool_call` decorator to intercept and format raw server data before the agent receives it.
- **Python-uv Support**: Built using the `uv` package manager for fast, reproducible environments.

## 🚀 Installation & Usage
1. Ensure the `mcp-server-tools` folder is located in the same parent directory as this repository.
2. Install dependencies:
   ```bash
   uv add mcp pydantic
   ```
3. Run the Agent:   
   ```bash
   uv run main.py
   ```

## 🔒 Security & Filtering
The agent is designed to automatically filter out any tools containing the string `"admin"` in their name.

### How to test the Security Alert:
1. Open `main.py`.
2. Change `tool_to_call = "get_weather"` to `tool_to_call = "admin_system_reboot"`.
3. Run `uv run main.py`.
4. The agent will trigger a **Security Alert** and block the execution.

## 🔗 System Architecture
This project is part of a decoupled system consisting of two repositories:
1. **[mcp-server-tools](https://github.com/LAjoyan/mcp-server-tools)**: The "Provider" (contains the tool logic).
2. **mcp-agent (This Repo)**: The "Orchestrator" (contains security filtering and middleware).

## 📊 Flow Diagram

This diagram illustrates the interaction between the two repositories and where the filtering/middleware logic occurs.

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant A as MCP Agent (Repo 2)
    participant M as Middleware (@wrap_tool_call)
    participant S as MCP Server (Repo 1)

    U->>A: Asks a question
    A->>S: Requests available tools
    S-->>A: Returns 5 Tools (including Admin)
    Note over A: FILTERING: Excludes 'admin_system_reboot'
    A->>M: Calls authorized tool (e.g., get_weather)
    M->>S: Forwards request to Server
    S-->>M: Returns raw tool result
    Note over M: MIDDLEWARE: Processes & formats output
    M-->>A: Returns wrapped/processed result
    A->>U: Delivers final answer to User
    