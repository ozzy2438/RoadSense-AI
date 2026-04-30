from __future__ import annotations

import os
import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def trace_step(name: str, **metadata: object) -> Iterator[dict[str, object]]:
    start = time.perf_counter()
    event = {"name": name, "metadata": metadata}
    try:
        yield event
    finally:
        event["duration_ms"] = round((time.perf_counter() - start) * 1000, 2)
        event["langfuse_host"] = os.getenv("LANGFUSE_HOST", "http://localhost:3001")
