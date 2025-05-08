FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bc \
    build-essential \
    clang \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Build stage
FROM base AS build

# Build all implementations
RUN make build

# Run tests (can be commented out for faster builds)
# RUN make test

# Final stage
FROM base AS final

# Copy built executables from build stage
COPY --from=build /app/pigame_c /app/pigame_c

# Install Python package
RUN pip install --no-cache-dir -e .

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Make sure pigame is executable
RUN chmod +x /app/pigame

# Set pigame as the entrypoint
ENTRYPOINT ["/app/pigame"]

# Default command
CMD ["--help"]
