import os
from logging import Logger
from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.core.config import settings
from app.core.responses import ORJSONResponse

logger: Logger = getLogger(__name__)


def get_trusted_hosts() -> list[str]:
    """
    Get the list of trusted proxy IPs from the environment variable 'FORWARDED_ALLOW_IPS'.

    It can use CIDR notation for subnets, e.g., "10.100.1.1/24", or a comma-separated list of IPs.

    Returns:
        list[str]: A list of trusted proxy IPs.
    """
    allowed_ips: str | list[str] = os.getenv("FORWARDED_ALLOW_IPS", ["127.0.0.1"])

    if isinstance(allowed_ips, str):
        allowed_ips = [ip.strip() for ip in allowed_ips.split(",") if ip.strip()]

    return allowed_ips


def create_app() -> "FastAPI":
    logger.debug("[Factory] FastAPI creating...")

    development_mode: bool = settings.project.environment == "development"

    app: FastAPI = FastAPI(
        default_response_class=ORJSONResponse,
        swagger_ui_parameters={
            "persistAuthorization": True,
            "filter": True,
            "displayRequestDuration": True,
            "defaultModelRendering": "model",
        },
        docs_url="/docs" if development_mode else None,
        redoc_url="/redoc" if development_mode else None,
        openapi_url="/openapi.json" if development_mode else None,
    )

    # Middlewares
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=get_trusted_hosts())  # type: ignore
    app.add_middleware(GZipMiddleware)  # type: ignore

    if development_mode:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,  # type: ignore
            allow_origins=settings.project.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/healthz", include_in_schema=False)
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    logger.debug("[Factory] FastAPI Created!")
    return app
