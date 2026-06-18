# ADR-002: PostGIS for Geofence Calculation

## Status
Accepted

## Context
Geo attendance requires checking if a user's location is within 20 meters of the company location. Options considered:
1. Haversine formula in Python
2. PostGIS ST_DWithin query

## Decision
Use PostGIS with ST_DWithin for geofence calculation despite it being infrastructure overhead for a single point-radius check.

## Consequences
- Demonstrates production-grade spatial query capability
- Enables future complex spatial queries (polygons, multiple locations) without architecture changes
- Requires PostGIS extension on PostgreSQL
- Spatial index (GIST) on location column improves query performance at scale
- Slight added complexity in migration and entity definition
