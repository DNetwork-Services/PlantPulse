FROM python:3.12-slim

# Prevents Python from writing .pyc files and buffers stdout —
# buffered stdout would delay logs from appearing in `docker logs`
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


# Copy requirements first, install, THEN copy the rest of the code.
# This ordering matters: Docker caches each layer, so if only your
# app code changes (not requirements.txt), the pip install layer
# is reused from cache instead of re-running — much faster rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD [ "uvicorn", "app.main:app","--host","0.0.0.0","--port","8000" ]

