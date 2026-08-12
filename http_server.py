import os

import uvicorn

from mcp_server import mcp


port = int(os.getenv("PORT", "10000"))

app = mcp.streamable_http_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )