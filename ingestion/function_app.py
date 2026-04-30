from __future__ import annotations

try:
    import azure.functions as func
    import azure.durable_functions as df
except Exception:  # pragma: no cover - local compile without Azure Functions installed
    func = None
    df = None


if func and df:
    app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)

    @app.blob_trigger(
        arg_name="blob",
        path="raw-documents/{name}",
        connection="AZURE_STORAGE_CONNECTION_STRING",
    )
    @app.durable_client_input(client_name="client")
    async def blob_ingest_starter(blob: func.InputStream, client: df.DurableOrchestrationClient):
        instance_id = await client.start_new(
            "ingestion_orchestrator",
            None,
            {"name": blob.name, "size": blob.length},
        )
        return {"instance_id": instance_id}
else:
    app = None
