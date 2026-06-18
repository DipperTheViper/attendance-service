FROM ghcr.io/astral-sh/uv:python3.14-alpine

WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev

EXPOSE 8100

CMD ["uv", "run", "python", "manage.py"]
