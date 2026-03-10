# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_PYTHON=python3.12 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Instala dependências com cache do BuildKit
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# --- Stage de Runtime ---
FROM python:3.12-slim-bookworm

# Copia o executável do uv para o runtime
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uv/bin/uv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PYTHON=/usr/local/bin/python3.12 \
    PATH="/uv/bin:/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app
COPY . .

# Garante que as credenciais e inventário existam
RUN touch coffeemaster.json coffeemaster_agent/inventory.json
# Expor a porta 1000 conforme solicitado
EXPOSE 1000

# Comando para rodar o servidor FastAPI CoffeeMaster Elite
CMD ["uv", "run", "python", "main.py"]
