# Financial Fraud Investigation RAG

A monorepo for an **evidence-grounded Retrieval-Augmented Generation (RAG) system for financial fraud investigation**, built with **Next.js**, **React**, **TypeScript**, **FastAPI**, **Python**, **pnpm**, **uv**, and **Turborepo**.

The system is designed to help fraud investigators analyze suspicious transactions by retrieving relevant evidence from customer transaction history, related account activity, historical fraud cases, and AML policies.

Rather than producing a generic chatbot response, the system will generate structured, investigator-ready case summaries with traceable evidence and source references.

---

## 1. Project Structure

The monorepo is organized into applications (`apps/`) and shared frontend packages (`packages/`):

```text
fraud-investigation-rag/
├── apps/
│   ├── web/                            # Investigator Dashboard (Next.js)
│   │   ├── app/                        # Next.js App Router
│   │   ├── public/                     # Static assets
│   │   ├── package.json                # Frontend dependencies and scripts
│   │   └── tsconfig.json               # TypeScript configuration
│   │
│   └── api/                            # Fraud Investigation API (FastAPI)
│       ├── src/
│       │   └── api/
│       │       ├── __init__.py
│       │       └── main.py             # FastAPI application entry point
│       ├── .python-version             # Python version used by uv
│       ├── pyproject.toml              # Python project and dependencies
│       └── uv.lock                     # Locked Python dependencies
│
├── packages/
│   ├── ui/                             # Shared React UI components
│   ├── eslint-config/                  # Shared ESLint configuration
│   └── typescript-config/              # Shared TypeScript configuration
│
├── .gitignore
├── .npmrc
├── package.json                        # Root monorepo scripts
├── pnpm-lock.yaml                      # Locked Node.js dependencies
├── pnpm-workspace.yaml                 # pnpm workspace configuration
├── turbo.json                          # Turborepo task configuration
└── README.md
```

As the project develops, additional directories will be introduced for database infrastructure, synthetic financial data, document ingestion, retrieval pipelines, evaluation, and deployment.

---

## 2. Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Turborepo
- pnpm

### Backend

- Python 3.12
- FastAPI
- Uvicorn
- uv

### Planned Data & RAG Infrastructure

- PostgreSQL
- pgvector
- SQLAlchemy
- Embedding models
- Semantic retrieval
- Keyword retrieval
- Hybrid retrieval
- Reranking
- LLM-based evidence synthesis
- Retrieval and RAG evaluation

---

## 3. Prerequisites

Ensure the following tools are installed before setting up the project:

- **Git**
- **Node.js**: `v24.x` or later
- **pnpm**: `v11.x` or later
- **Python**: Python `3.12` is used by the backend
- **uv**: Python package and environment manager

Check the installed versions:

```bash
git --version
node --version
pnpm --version
python --version
uv --version
```

> The system-wide Python version does not need to be Python 3.12. The backend uses `uv` to manage its Python environment independently.

---

## 4. Local Setup Guide

### Step 1: Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/KripaGurung/fraud-investigation-rag.git
```

Move into the project directory:

```bash
cd fraud-investigation-rag
```

---

### Step 2: Install Monorepo Dependencies

Install the Node.js dependencies from the repository root:

```bash
pnpm install
```

This installs dependencies for the Turborepo workspace, including the Next.js frontend and shared packages.

#### Windows PowerShell

If PowerShell prevents the `pnpm` script from running because of the execution policy, use:

```powershell
pnpm.cmd install
```

---

### Step 3: Install uv

The backend uses `uv` to manage Python versions, virtual environments, and Python dependencies.

#### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart the terminal if `uv` is not immediately available.

Verify the installation:

```bash
uv --version
```

If `uv` is already installed, this step can be skipped.

---

### Step 4: Set Up the FastAPI Backend

Move into the backend application:

```bash
cd apps/api
```

Synchronize the Python environment and install the locked dependencies:

```bash
uv sync
```

`uv` will use the backend project configuration to create and synchronize the local Python environment.

The backend is configured to use Python 3.12 through:

```text
apps/api/.python-version
```

Verify the Python version used by the backend:

```bash
uv run python --version
```

It should report Python `3.12.x`.

---

### Step 5: Run the FastAPI Backend

From the `apps/api` directory, start the FastAPI development server:

```bash
uv run uvicorn api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

Stop the development server with:

```text
Ctrl + C
```

---

### Step 6: Run the Frontend

Open another terminal and navigate to the repository root.

Start the Turborepo development environment:

```bash
pnpm dev
```

The Next.js application will normally be available at:

```text
http://localhost:3000
```

Stop the development server with:

```text
Ctrl + C
```

---

## 5. Development Workflow

The frontend and backend currently run in separate terminals.

### Terminal 1 — Frontend

From the repository root:

```bash
pnpm dev
```

### Terminal 2 — Backend

Navigate to the API application:

```bash
cd apps/api
```

Start FastAPI:

```bash
uv run uvicorn api.main:app --reload
```

The current local development architecture is:

```text
Browser
   │
   ▼
Next.js Web App
localhost:3000
   │
   │ HTTP API
   ▼
FastAPI
localhost:8000
```

Database and RAG services will be introduced in later development phases.

---

## 6. Useful Commands

| Command                                | Run From        | Description                                         |
| -------------------------------------- | --------------- | --------------------------------------------------- |
| `pnpm install`                         | Repository root | Install Node.js workspace dependencies              |
| `pnpm dev`                             | Repository root | Start Turborepo development tasks                   |
| `pnpm build`                           | Repository root | Build workspace applications and packages           |
| `pnpm lint`                            | Repository root | Run linting across the workspace                    |
| `pnpm check-types`                     | Repository root | Run TypeScript type checking                        |
| `pnpm format`                          | Repository root | Format TypeScript, TSX, and Markdown files          |
| `uv sync`                              | `apps/api`      | Synchronize the Python environment and dependencies |
| `uv add <package>`                     | `apps/api`      | Add a Python dependency                             |
| `uv run python --version`              | `apps/api`      | Check the Python version used by the backend        |
| `uv run uvicorn api.main:app --reload` | `apps/api`      | Start the FastAPI development server                |

---

## 7. Project Goals

The project aims to explore and implement:

- Multi-source retrieval across structured and unstructured financial data
- Retrieval-Augmented Generation (RAG)
- Historical fraud case retrieval
- AML policy retrieval
- Semantic and keyword search
- Hybrid retrieval
- Evidence reranking
- Supporting evidence retrieval
- Counter-evidence retrieval
- Contradiction-aware retrieval
- Missing-evidence detection
- Source citation and provenance tracking
- Evidence-grounded investigation reports
- Retrieval and RAG evaluation

---

## 8. Project Roadmap

The project will be developed incrementally so that each stage introduces a new part of the RAG and fraud investigation architecture.

### Phase 1 — Foundation

- [x] Create GitHub repository
- [x] Initialize Turborepo monorepo
- [x] Set up Next.js frontend
- [x] Set up FastAPI backend
- [x] Configure pnpm
- [x] Configure uv and Python 3.12
- [ ] Connect frontend and backend

### Phase 2 — Financial Data Layer

- [ ] Design customer schema
- [ ] Design account schema
- [ ] Design transaction schema
- [ ] Design fraud alert schema
- [ ] Generate synthetic banking data
- [ ] Add PostgreSQL
- [ ] Add database migrations
- [ ] Implement transaction retrieval

### Phase 3 — Basic RAG

- [ ] Build AML policy corpus
- [ ] Build historical fraud case corpus
- [ ] Implement document ingestion
- [ ] Implement document chunking
- [ ] Generate embeddings
- [ ] Add pgvector
- [ ] Implement semantic retrieval
- [ ] Add source citations

### Phase 4 — Advanced Retrieval

- [ ] Implement keyword retrieval
- [ ] Implement hybrid retrieval
- [ ] Add metadata filtering
- [ ] Add reranking
- [ ] Implement query decomposition
- [ ] Combine structured SQL retrieval with document retrieval

### Phase 5 — Evidence-Aware Investigation

- [ ] Retrieve supporting evidence
- [ ] Retrieve counter-evidence
- [ ] Detect contradictory evidence
- [ ] Detect missing evidence
- [ ] Generate structured investigation reports
- [ ] Validate evidence citations and provenance

### Phase 6 — Evaluation

- [ ] Create retrieval ground truth
- [ ] Measure Precision@K
- [ ] Measure Recall@K
- [ ] Measure MRR
- [ ] Measure NDCG
- [ ] Compare vector, hybrid, and reranked retrieval
- [ ] Evaluate contradiction-aware retrieval
- [ ] Evaluate generated investigation reports

---

## 9. Planned System Architecture

The target investigation workflow is:

```text
Suspicious Transaction / Alert
              │
              ▼
      Investigation Request
              │
              ▼
       Evidence Planning
              │
       ┌──────┼──────────────┐
       │      │              │
       ▼      ▼              ▼
 Transaction  Historical    AML
   History    Fraud Cases  Policies
       │      │              │
       └──────┼──────────────┘
              │
              ▼
       Evidence Retrieval
              │
       ┌──────┼─────────────┐
       │      │             │
       ▼      ▼             ▼
 Supporting  Conflicting   Missing
 Evidence    Evidence      Evidence
       │      │             │
       └──────┼─────────────┘
              │
              ▼
      Evidence Normalization
              │
              ▼
        Evidence Ranking
              │
              ▼
    Evidence-Grounded Generation
              │
              ▼
    Structured Investigation Case
              │
              ▼
      Investigator Dashboard
```

The architecture will evolve as each project phase is implemented.

---

## 10. RAG Evaluation Strategy

The project will eventually compare multiple retrieval approaches rather than relying on a single vector-search implementation.

Planned retrieval experiments include:

```text
Vector Retrieval
       │
       ▼
Hybrid Retrieval
       │
       ▼
Hybrid + Reranking
       │
       ▼
Contradiction-Aware Retrieval
```

Retrieval quality will be evaluated using metrics such as:

- Precision@K
- Recall@K
- Mean Reciprocal Rank (MRR)
- Normalized Discounted Cumulative Gain (NDCG)

Generation quality will also be evaluated for evidence grounding, citation correctness, and investigation completeness.

---

## 11. Project Vision

A traditional RAG application typically follows:

```text
Question
   │
   ▼
Retrieve Documents
   │
   ▼
LLM
   │
   ▼
Answer
```

This project aims to go further by treating retrieval as part of an investigation process:

```text
Suspicious Activity
        │
        ▼
What evidence do we need?
        │
        ▼
Retrieve Evidence
        │
        ├── What supports the suspicion?
        ├── What contradicts the suspicion?
        └── What evidence is still missing?
        │
        ▼
Evaluate Evidence
        │
        ▼
Generate Case File
        │
        ▼
Human Investigator
```

The goal is not to build another financial chatbot.

The goal is to build an **auditable financial investigation RAG system where generated conclusions can be traced back to retrieved evidence**.
