from __future__ import annotations

from fastapi import Header, HTTPException


async def require_operator(authorization: str | None = Header(default=None)) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="missing authorization header")
    return "local-operator"
