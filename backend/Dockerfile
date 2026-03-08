FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install dependencies into a fixed virtualenv so bind mounts do not hide them.
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_DEV=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN uv venv /opt/venv

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --active

COPY . .
RUN uv sync --locked --active

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
