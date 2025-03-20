FROM python:3.13.0-slim-bookworm AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app

WORKDIR /app
RUN uv sync --all-extras
# RUN uv sync --compile-bytecode

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Run the application
CMD ["uvicorn" ,"main.asgi:application", "--reload" "--host=0.0.0.0"]

# # Install uv
# FROM python:3.13-slim
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# # Change the working directory to the `app` directory
# WORKDIR /app

# # Install dependencies
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --all-extras

# # Copy the project into the image
# ADD . /app

# # Sync the project
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync --frozen
# RUN uv sync --compile-bytecode

# Run the application
# CMD ["uvicorn" ,"main.asgi:application", "--reload"]