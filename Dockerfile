
FROM astral/uv:python3.14-alpine
#FROM docker.arvancloud.ir/astral/uv:python3.13-alpine


WORKDIR /src
COPY . .
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

EXPOSE 8100

CMD ["uv", "run", "python", "manage.py"]
