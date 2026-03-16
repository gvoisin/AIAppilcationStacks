# App Server

Backend server for the Stack demo. It exposes:
- an A2A dynamic agent endpoint (`/agent`)
- an A2A LLM endpoint (`/llm`)
- traditional JSON endpoints (`/traditional/*`)
- config endpoints to tune dynamic-agent behavior at runtime (`/agent/config`)

It is built with Starlette + A2A SDK, and uses OCI GenAI + Oracle DB for LLM/RAG capabilities.

## Requirements

- Python `>=3.13`
- `uv` package manager
- OCI credentials and access to GenAI endpoint
- Oracle DB credentials/wallet (required for RAG + NL2SQL tools)

## Environment Setup

1. From `app/server`, copy the env template:
```bash
cp .env.example .env
```

2. Fill in the values in `.env`:
```env
COMPARTMENT_ID=<your-compartment-id>
AUTH_PROFILE=<oci-config-profile>
SERVICE_ENDPOINT=https://inference.generativeai.us-chicago-1.oci.oraclecloud.com

DB_PASSWORD=<your-password>
DB_WALLET_PATH=<absolute-path-to-wallet>
DB_WALLET_PASSWORD=<wallet-password>
DB_USER=<db-user>
DB_DSN=<db-dsn>
```

## Install Dependencies

```bash
uv sync
```

## Run the Server

From `app/server`:

```bash
uv run __main__.py
```

Optional flags:

```bash
uv run __main__.py --host localhost --port 10002 --mock
```

`--mock` starts credential-free mock executors for UI testing.

## Key Routes

- `GET/POST/DELETE /agent/config`: read, update, or reset dynamic graph config
- `POST /agent/*`: A2A dynamic graph agent
- `POST /llm/*`: A2A LLM agent
- `GET /traditional`
- `GET /traditional/energy`
- `GET /traditional/trends`
- `GET /traditional/timeline`
- `GET /traditional/industry`
- `GET /rag_docs/*`: static access to source PDFs used by RAG

## Optional: Load RAG Documents Into DB

If you want semantic search over the PDFs in `core/rag_docs`:

```bash
uv run core/setup_rag.py
```

This creates/recreates the embedding table and indexes all PDFs.

## Tests

Install dev dependencies and run tests:

```bash
uv pip install -e ".[dev]"
uv run pytest tests -v
```

## Project Structure

```text
app/server/
|-- __main__.py                     # Server entrypoint (mounts /agent, /llm, /traditional)
|-- pyproject.toml                  # Dependencies and project metadata
|-- mock_executors.py               # Mock executors for local/UI testing
|-- chat_app/                       # LLM agent + tools (RAG + NL2SQL)
|   |-- llm_executor.py
|   |-- main_llm.py
|   |-- nl2sql_agent.py
|   `-- rag_tool.py
|-- dynamic_app/                    # Dynamic multi-agent graph orchestration
|   |-- dynamic_agents_graph.py
|   |-- dynamic_graph_executor.py
|   |-- back_agents_graph/
|   `-- ui_agents_graph/
|-- core/                           # Shared providers, prompts, schemas, base classes
|   |-- base_agent.py
|   |-- gen_ai_provider.py
|   |-- traditional_data_provider.py
|   `-- dynamic_app/
|-- database/
|   `-- connections.py              # Oracle DB connection/pool utilities
|-- traditional_app/
|   `-- data_provider.py            # Traditional endpoint payload builders
`-- tests/
    |-- test_catalog.py
    `-- test_ui_orchestrator_agent.py
```

## Notes for New Contributors

- Dynamic graph configuration schema/defaults are in `core/dynamic_app/dynamic_struct.py`.
- A2A capability/skill metadata is in `core/dynamic_app/a2a_config_provider.py`.
- The server loads `.env` automatically on startup.
