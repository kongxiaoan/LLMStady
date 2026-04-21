from __future__ import annotations

import uvicorn

from llm.config import load_settings


def main() -> None:
    settings = load_settings()

    uvicorn.run(
        "llm.http.app:app",
        host=settings.http_host,
        port=settings.http_port,
        reload=False,
        factory=False,
    )

