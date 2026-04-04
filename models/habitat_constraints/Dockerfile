FROM python:3.12-slim
WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY src/ ./src/

RUN uv sync --extra api --no-dev

CMD ["uv", "run", "uvicorn", "habitat_constraints.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
