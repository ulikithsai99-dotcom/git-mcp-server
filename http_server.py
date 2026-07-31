import uvicorn

from mcp_server import mcp

if __name__ == "__main__":
    uvicorn.run(
        mcp.streamable_http_app(),
        host=mcp.settings.host,
        port=mcp.settings.port,
        log_level="info",
    )