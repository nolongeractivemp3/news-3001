FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv

# Add uv to the system PATH
ENV PATH="/uvbin:${PATH}"

WORKDIR /app
COPY . .

# Install deps if you have the files, otherwise skip
RUN if [ -f pyproject.toml ]; then uv sync --frozen; fi

CMD ["uv", "run", "python", "server.py"]
