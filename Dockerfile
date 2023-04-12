FROM python:3.11-slim AS base

WORKDIR /app

# Security
ENV USERNAME=user

RUN groupadd -r $USERNAME && \
    useradd -r -g $USERNAME $USERNAME

FROM base AS builder

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN set -eux; \
    apt-get update && \
    apt-get install --yes --no-install-recommends git && \
    # Upgrade pip and wheel
    /opt/venv/bin/python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel && \
    # Install the dependencies
    pip install --no-cache-dir -r requirements.txt && \
    # Clean up git
    apt-get remove --yes git && \
    apt-get autoremove --yes && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM base AS app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

USER $USERNAME

CMD ["python", "app/api.py"]