# temp stage
FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.10-slim

RUN addgroup --gid 10000 --system app && \
    adduser --home /app --shell /bin/false --disabled-password --uid 10000 --system --group app

USER app

WORKDIR /app

COPY --from=builder /app/wheels wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache wheels/*
