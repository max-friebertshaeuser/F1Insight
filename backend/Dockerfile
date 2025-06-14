## Stage 1: Base build stage
#FROM python:3.13-slim AS builder
#
## Create the app directory
#RUN mkdir /app
#
## Set the working directory
#WORKDIR /app
#
## Set environment variables to optimize Python
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
## Upgrade pip and install dependencies
#RUN pip install --upgrade pip
#
## Copy the requirements file first (better caching)
#COPY requirements.txt /app/
#
## Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Stage 2: Production stage
#FROM python:3.13-slim
#
## install cron
#RUN apt-get update && apt-get install -y cron && useradd -m -r appuser && mkdir /app && touch /var/run/crond.pid && chown -R appuser:appuser /app /var/run/crond.pid && rm -rf /var/lib/apt/lists/*
#
##RUN useradd -m -r appuser && \
##   mkdir /app && \
##   chown -R appuser /app
#
## Copy the Python dependencies from the builder stage
#COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
#COPY --from=builder /usr/local/bin/ /usr/local/bin/
#
## Set the working directory
#WORKDIR /app
#
## Copy application code
#COPY --chown=appuser:appuser . .
#
## Set environment variables to optimize Python
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
## Copy and make entrypoint executable
#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh
#
## Ensure cron is installed (wenn nicht schon geschehen)
#RUN apt-get update \
# && apt-get install -y cron \
# && rm -rf /var/lib/apt/lists/*
#
## Leave root so cron darf starten
#USER root
#
## Use entrypoint to start cron + gunicorn
#ENTRYPOINT ["/entrypoint.sh"]
#
## Switch to non-root user
#USER appuser
#
## Expose the application port
#EXPOSE 8000
#
## Start the application using Gunicorn
##CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "f1hub.wsgi:application"]
#CMD ["sh", "-c", "cron && gunicorn --bind 0.0.0.0:8000 --workers 3 f1hub.wsgi:application"]

# Stage 1: Base
FROM python:3.13-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-slim

# install cron, create appuser & PID‐File
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/* && useradd -m -r appuser && touch /var/run/crond.pid && chown appuser:appuser /var/run/crond.pid

WORKDIR /app
# 3) Copy Python libs
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# 4) Copy app code & entrypoint
COPY --chown=appuser:appuser . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 5) Expose & Entrypoint
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
