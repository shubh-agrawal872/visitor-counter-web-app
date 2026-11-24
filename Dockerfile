# Multi-stage and slim base for minimal footprint (Cost Optimization Technique #3)
FROM python:3.11-slim

# Metadata
LABEL maintainer="Cloud Computing Project Student"
LABEL description="Visitor Counter Web App with Flask and Redis"

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set working directory
WORKDIR /app

# Install dependencies first (leverage Docker layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for security best practices
RUN useradd -u 10001 -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Copy application source code
COPY --chown=appuser:appuser app.py /app/

# Expose web service port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')" || exit 1

# Launch with production WSGI server (Gunicorn) with 2 workers and 2 threads
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "30", "app:app"]
