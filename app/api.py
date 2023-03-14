from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from starlette.middleware import Middleware
from uvicorn.config import LOGGING_CONFIG

import routes
from core import config

# Middleware 具有順序性，由上而下依序對所有 request 進行處理
middleware: list[Middleware] = [
    # Middlewares
]

if config.get("DEBUG", False):
    app: FastAPI = FastAPI(middleware=middleware)

else:
    app: FastAPI = FastAPI(
        middleware=middleware, openapi_url="", docs_url="", redoc_url=""
    )

# 單一引入，避免在此處進行 include_route
# 避免維護困難
app.include_router(routes.routes)


def initialize_data():
    """Inject initial data into database."""
    pass


def initialize() -> None:
    """Check if we need to create database and inject initial data."""
    logger.info("Initializing...")
    logger.debug("Checking database...")
    logger.warning("Database not found. Creating database...")
    logger.critical("Database created. Injecting initial data...")
    logger.error("Initial data injected.")


if __name__ == "__main__":
    # Setup logging
    if config.logger_config:
        log_config: Any = str(config.logger_config)

    else:
        logger.warning("Logger config file not found. Using default config.")
        log_config: Any = LOGGING_CONFIG

    # App startup
    initialize()
    uvicorn.run(
        "api:app",
        reload=config.get("RELOAD"),
        host=config.get("HOST"),
        port=config.get("PORT"),
        log_config=log_config,
    )
