from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response


async def add_process_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["x-process-time-ms"] = f"{(time.perf_counter() - start) * 1000:.2f}"
    return response
