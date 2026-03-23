# Multi-stage build for VyFwMatch - VyOS Firewall Policy Matcher
# Stage 1: Builder
FROM python:3.14-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt setup.py ./
COPY vyfwmatch/ ./vyfwmatch/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Stage 2: Runtime
FROM python:3.14-slim

# Set labels for container metadata
LABEL org.opencontainers.image.title="VyFwMatch"
LABEL org.opencontainers.image.description="VyOS Firewall Policy Matcher - Parse and test VyOS firewall configurations"
LABEL org.opencontainers.image.version="2.0.0"
LABEL org.opencontainers.image.authors="VyFwMatch Contributors"
LABEL org.opencontainers.image.url="https://github.com/rbelkhir/vyos-fw-match"
LABEL org.opencontainers.image.source="https://github.com/rbelkhir/vyos-fw-match"
LABEL org.opencontainers.image.licenses="MIT"

RUN useradd -m -u 1000 -s /bin/bash vyfwmatch
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin/vyfwmatch /usr/local/bin/vyfwmatch

COPY --chown=vyfwmatch:vyfwmatch vyfwmatch/ ./vyfwmatch/
COPY --chown=vyfwmatch:vyfwmatch vyos-1x/python ./vyos-1x/python
COPY --chown=vyfwmatch:vyfwmatch setup.py README.md LICENSE ./

RUN mkdir -p /config && chown vyfwmatch:vyfwmatch /config

USER vyfwmatch
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

VOLUME ["/config"]

# Default command shows help
ENTRYPOINT ["vyfwmatch"]
CMD ["--help"]
