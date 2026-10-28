FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends g++ gdb python3 python3-venv ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv && /venv/bin/pip install --no-cache-dir fastapi==0.115.6 "uvicorn[standard]==0.34.0"

WORKDIR /srv
COPY cpp ./cpp
COPY app ./app

RUN useradd -m -u 10001 runner
USER runner
EXPOSE 8000
CMD ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
