# RoadSense AI Project Plan

## Scope

Build a credible portfolio-grade implementation of an agentic RAG claims triage platform. The first milestone is a complete repository scaffold with runnable local API and frontend, mock tools, evaluation scripts, infrastructure placeholders, and CI.

## Milestones

1. Local demo: FastAPI SSE triage endpoint, mock retrieval, guardrails, and Next.js console.
2. Ingestion: Durable Functions orchestration with PDF parse, chunking, PII masking, embeddings, and search indexing.
3. Evaluation: Golden dataset, policy-grounded judge, promptfoo regression suite, and CI thresholds.
4. Observability: Langfuse traces, latency and cost counters, audit-event model.
5. Azure deployment: Bicep modules, container images, Helm chart, and staged GitHub Actions workflows.

## Demo Narrative

An operator receives a member message, watches the agent graph run, sees policy evidence and tool calls, and gets a final triage recommendation with confidence, safety flags, and human-handoff rationale.
