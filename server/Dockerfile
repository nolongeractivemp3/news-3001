FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Copy only dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (cached unless pyproject.toml or uv.lock change)
RUN uv sync --locked --no-install-project

# Now copy the rest of the source code
COPY . .

# Install the project itself
RUN uv sync --locked

CMD ["uv", "run", "server.py"]
