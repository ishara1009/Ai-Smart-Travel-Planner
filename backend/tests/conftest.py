import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-that-is-long-enough-123")
os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017")
