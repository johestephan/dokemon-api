# Multi-stage build for minimal image size
FROM python:3.11-slim AS builder

# Install only essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download only the Docker CLI binary (not the entire Docker suite)
RUN curl -fsSL "https://download.docker.com/linux/static/stable/x86_64/docker-24.0.7.tgz" | \
    tar -xzC /tmp && \
    mv /tmp/docker/docker /usr/local/bin/docker && \
    chmod +x /usr/local/bin/docker && \
    rm -rf /tmp/docker

# Production stage - minimal runtime image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    DOKEMON_HOST=0.0.0.0 \
    DOKEMON_PORT=9090 \
    DOKEMON_DEBUG=false

# Set work directory
WORKDIR /app

# Copy only the Docker CLI binary from builder stage
COPY --from=builder /usr/local/bin/docker /usr/local/bin/docker

# Copy requirements first for better layer caching
COPY src/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ ./src/

# Copy deployment configuration files (version.txt should be accessible from src directory)
COPY version.txt ./src/

# Create directory for user data
RUN mkdir -p /app/data

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# For Docker socket access, add app user to docker group
RUN groupadd -g 999 docker || true
RUN usermod -a -G docker app

# Make data directory accessible
RUN chmod 755 /app/data

# Set Python path to include src directory
ENV PYTHONPATH="/app/src"

# Switch to app user for runtime
USER app

# Set working directory to src for proper imports
WORKDIR /app/src

# Expose port
EXPOSE 9090

# Health check using Python instead of curl to save space
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9090/health')" || exit 1

# Default command - use Gunicorn for production (run from src directory)
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
