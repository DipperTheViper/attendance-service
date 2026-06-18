# ADR-003: Celery + Redis for Async SMS with Retry

## Status
Accepted

## Context
SMS notification must be sent on check-in without blocking the HTTP response. Failure must trigger retry. Options considered:
1. asyncio background task (FastAPI BackgroundTasks)
2. Celery with Redis broker

## Decision
Use Celery with Redis as broker and backend. Tasks are pushed to Redis queue, worker processes them independently with configurable max_retries and exponential backoff.

## Consequences
- HTTP response is not blocked by SMS sending
- Retry logic is production-grade and configurable
- Requires Celery worker process alongside the app
- Redis serves dual purpose (auth sessions + task queue)
- Pseudocode SMS provider can be replaced with real provider without architecture change
