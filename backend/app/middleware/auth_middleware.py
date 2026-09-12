"""Authentication is implemented as a FastAPI dependency in api/dependencies.py.

Keeping authentication at the dependency layer makes protected routes explicit in
OpenAPI and avoids decoding tokens for public endpoints.
"""
