# Enterprise Intelligence GraphRAG

A GraphRAG (Graph-based Retrieval-Augmented Generation) backend that answers natural-language questions about an organization — its employees, projects, tasks, customers, departments, companies, documents, and skills — by combining a **Neo4j knowledge graph** with an **LLM (Groq)** for answer generation.

Instead of chunking documents into a vector store, the system models enterprise entities and their relationships as a graph, resolves a question to the relevant entity, pulls its connected context straight from the graph, and hands that context to the LLM to produce a grounded answer.

## How it works

```
Question
   │
   ▼
QueryParser        — LLM extracts { entity_type, name } from the question
   │                 (reuses the previous entity for follow-up/vague references)
   ▼
EntityResolver      — resolves the (type, name) pair to a concrete node ID in Neo4j
   │                 (falls back to searching all entity types if the guess misses)
   ▼
GraphContextBuilder  — runs Cypher queries to pull the entity + its related nodes
   ▼
context_formatter   — formats the graph data into readable text context
   ▼
prompt_builder      — builds the final LLM prompt from the context + question
   ▼
LLMClient (Groq)    — generates the answer
   ▼
Answer
```

All of this is orchestrated by `RAGPipeline` in [app/pipeline.py](app/pipeline.py).

## Tech stack

| Layer | Technology |
|---|---|
| Graph database | Neo4j |
| Relational database | MySQL (via SQLAlchemy) — stores chat history |
| LLM | Groq (via `langchain-groq`) |
| API | FastAPI |
| Config | pydantic-settings (`.env`) |

## Project structure

```
backend/
├── main.py                    # CLI entry point — interactive Q&A loop
├── app/
│   ├── api/main.py            # FastAPI app (/chat endpoints)
│   ├── core/config.py         # Settings loaded from .env
│   ├── db/                    # SQLAlchemy models + session (chat history in MySQL)
│   ├── graph/                 # Neo4j client, schema constraints, schema builder
│   ├── ingestion/              # Loads sample JSON data into the graph (nodes + relationships)
│   ├── retrieval/
│   │   ├── query_parser.py     # LLM-based entity type/name extraction
│   │   ├── entity_resolver.py  # Resolves entity name -> graph node ID
│   │   ├── graph_retriever.py  # Cypher queries for entity lookups
│   │   ├── context_builder.py  # Builds full graph context per entity type
│   │   ├── context_formatter.py# Formats graph context into text
│   │   └── prompt_builder.py   # Builds the final LLM prompt
│   ├── llm/client.py           # ChatGroq wrapper with retry/backoff
│   └── pipeline.py             # Orchestrates the full RAG flow
├── scripts/
│   ├── create_schema.py        # Creates Neo4j constraints
│   ├── ingest_data.py          # Loads data/sample/*.json into Neo4j
│   ├── run_eval.py             # LLM-as-judge evaluation over data/eval/test_queries.json
│   └── test_*.py               # Manual smoke tests for individual components
└── data/
    ├── sample/                 # Sample enterprise dataset (companies, employees, projects, ...)
    └── eval/                   # Evaluation queries and results
```

## Data model

The graph is built from these node types, connected by relationships such as `WORKS_AT`, `MEMBER_OF`, `HAS_SKILL`, `ASSIGNED_TO`, `MANAGES`, `SERVES`, and `RELATED_TO`:

- **Company** — organizations
- **Department** — belongs to a company
- **Employee** — belongs to a department/company, has skills, reports to a manager
- **Skill** — linked to employees
- **Project** — linked to a company, customer, and employees
- **Task** — linked to a project and an assigned employee
- **Customer** — linked to projects
- **Document** — linked to projects

## Setup

### 1. Prerequisites

- Python 3.10+
- A running Neo4j instance (local or Aura)
- A running MySQL instance
- A Groq API key

### 2. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in `backend/` with:

```env
NEO4J_URI=neo4j+s://<your-instance>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<password>
NEO4J_DATABASE=neo4j

GROQ_API_KEY=<your-groq-key>
GROQ_MODEL=openai/gpt-oss-20b

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=<user>
MYSQL_PASSWORD=<password>
MYSQL_DATABASE=<database>
```

### 4. Create the graph schema

```bash
python -m scripts.create_schema
```

### 5. Ingest the sample data

```bash
python -m scripts.ingest_data
```

This loads the companies, departments, employees, skills, projects, tasks, customers, and documents from `data/sample/*.json` into Neo4j, then wires up all relationships.

## Running

### CLI

```bash
python main.py
```

Ask questions interactively; type `exit` to quit.

### API

```bash
uvicorn app.api.main:app --reload
```

- `POST /chat` — `{ "question": "..." }` → runs the pipeline and stores the exchange in MySQL
- `GET /chat?limit=20` — returns the most recent chat exchanges

## Evaluation

```bash
python -m scripts.run_eval
```

Runs the pipeline against `data/eval/test_queries.json` and uses the LLM as a judge to score each answer against its retrieved context, writing results to `data/eval/result.json`.
