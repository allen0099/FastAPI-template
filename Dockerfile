FROM python:3.12-slim AS base

ENV VIRTUAL_ENV="/opt/venv"
ENV UV_PROJECT_ENVIRONMENT="$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM ghcr.io/astral-sh/uv:latest AS uv

FROM base AS library

COPY --from=uv /uv /uvx /bin/

# Install git so we can install packages from git repos
RUN apt-get update && \
    apt-get install --yes --no-install-recommends git

COPY pyproject.toml .

RUN uv sync --no-dev

FROM base AS production

# Upgrade components
RUN pip install --upgrade --no-cache-dir pip

# Install curl for healthchecks
RUN apt-get update && \
    apt-get install --yes --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy python dependencies from the library stage
COPY --from=library /opt/venv /opt/venv

# TODO: change to non-root user

FROM production

WORKDIR /app

# Copy entrypoint script
COPY docker-entrypoint.sh /

# Copy application code
COPY . /app

# Expose default proxy headers and set production environment
ENV PROJECT__ENVIRONMENT="production"
ENV FORWARDED_ALLOW_IPS="127.0.0.1"

ENTRYPOINT ["/docker-entrypoint.sh"]
