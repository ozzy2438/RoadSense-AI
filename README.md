# RoadSense AI

[![ci](https://github.com/ozzy2438/RoadSense-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/ozzy2438/RoadSense-AI/actions/workflows/ci.yml)

RoadSense AI is an agentic RAG platform for roadside assistance and insurance claim triage. It simulates an RACV-style operating environment: member requests arrive through chat, email, or call transcripts, and the system retrieves policy evidence, checks risk signals, calls operational tools, and streams an auditable recommendation to an operator.

## What This Shows

- Event-driven Azure ingestion with Blob Storage, Event Grid, Durable Functions, Document Intelligence, Azure AI Search, and Cosmos DB.
- Agentic orchestration with a router, retrieval, policy reasoning, action, and guardrail flow.
- Production API surface using FastAPI, Pydantic schemas, and SSE streaming.
- TypeScript operator console for live agent-step visibility.
- Evaluation gates with RAGAS-style metrics, promptfoo regression tests, and a golden dataset.
- Responsible AI controls: PII masking, prompt injection detection, audit logs, human handoff, and model-gateway configuration.

## Repository Structure

```text
roadsense-ai/
├── api/                 # FastAPI API and streaming routes
├── agents/              # Agent state, graph, router, retrieval, tools, guardrails
├── data/                # Dataset download, transforms, golden-set generation
├── deploy/              # Dockerfiles and Helm chart
├── eval/                # RAGAS/promptfoo/LLM judge harness
├── frontend/            # Next.js 14 operator console
├── ingestion/           # Azure Functions and Durable Functions activities
├── infra/               # Azure Bicep infrastructure modules
├── observability/       # Langfuse client wrappers and dashboard assets
└── security/            # Presidio and prompt-injection utilities
```

## Quick Start

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
docker compose up -d redis postgres
uvicorn api.main:app --reload --port 8000
```

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the console at `http://localhost:3000` and submit a sample request such as:

```text
Member is stranded near Ballarat after a collision. They mention comprehensive cover and need towing.
```

## API Example

```bash
curl -N -X POST http://localhost:8000/triage/stream \
  -H "content-type: application/json" \
  -d '{"member_id":"M-10042","channel":"chat","message":"I hit a kangaroo near Geelong and need a tow. Am I covered?"}'
```

The endpoint emits Server-Sent Events for each agent step, including retrieved evidence, safety decisions, action-tool output, and final handoff guidance.

## Evaluation Targets

The project is designed around concrete production-style gates:

| Metric | Target |
| --- | ---: |
| Faithfulness | >= 0.88 |
| Context precision | >= 0.80 |
| Prompt injection catch rate | >= 0.95 |
| P95 triage latency | <= 5.0s |
| Cost per triage | <= USD 0.02 |

Run local checks:

```bash
python data/build_golden_set.py --output eval/golden_set.jsonl
python eval/ragas_runner.py --input eval/golden_set.jsonl
python eval/llm_judge.py --input eval/golden_set.jsonl
```

## Azure Deployment Shape

The Bicep files under `infra/` provision the application skeleton in `australiaeast`:

- Storage account and blob containers for raw policy documents and transcripts.
- Azure AI Search index for hybrid retrieval.
- Azure Functions with Durable Functions orchestration for ingestion.
- Cosmos DB for audit events, conversation state, and prompt-version metadata.
- Azure OpenAI account placeholder for model deployments.
- AKS cluster placeholder for the FastAPI and worker workloads.

Deploy commands are intentionally explicit:

```bash
az login
az account set --subscription <subscription-id>
./infra/deploy.sh roadsense-dev australiaeast
```

## Responsible AI Notes

Every triage response should carry source chunk IDs, prompt version, model name, risk flags, confidence score, and a human-handoff decision. PII is masked before indexing. Prompt injection attempts are recorded in the audit stream with sanitized input and detector rationale.
