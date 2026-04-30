from __future__ import annotations

try:
    import azure.durable_functions as df
except Exception:  # pragma: no cover
    df = None


def orchestrator_function(context):
    document = context.get_input()
    parsed = yield context.call_activity("parse_pdf", document)
    masked = yield context.call_activity("pii_mask", parsed)
    chunks = yield context.call_activity("chunk_embed", masked)
    result = yield context.call_activity("index_search", chunks)
    return result


main = df.Orchestrator.create(orchestrator_function) if df else orchestrator_function
