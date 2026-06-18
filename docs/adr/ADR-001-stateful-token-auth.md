# ADR-001: Stateful Token Authentication via Redis

## Status
Accepted

## Context
The requirement explicitly demands stateful, token-based authentication capable of handling high traffic. Stateless JWT was the alternative but does not support instant token revocation and requires additional infrastructure for blacklisting.

## Decision
Implement stateful token auth by storing opaque tokens in Redis with TTL. On each request, token is looked up in Redis to retrieve user_uuid. Logout deletes the token immediately.

## Consequences
- Instant token revocation on logout
- Requires Redis infrastructure
- Horizontal scaling supported via shared Redis instance
- Slightly higher latency per request due to Redis lookup (mitigated by Redis speed)
- No JWT decode overhead
