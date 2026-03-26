# Multi-stage build for VyFwMatch - VyOS Firewall Policy Matcher

# Stage 1: Build native binary (ipaddrcheck)
FROM debian:bookworm AS binary-builder

WORKDIR /build

# Install build dependencies for ipaddrcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    autoconf automake libtool gcc make pkg-config \
    libcidr-dev libpcre2-dev check \
    && rm -rf /var/lib/apt/lists/*

# Build ipaddrcheck
COPY ipaddrcheck/ /build/ipaddrcheck/
WORKDIR /build/ipaddrcheck
RUN autoreconf -i && \
    ./configure && \
    make

# Stage 2: Python wheel builder
FROM python:3.14-slim AS wheel-builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt setup.py ./
COPY vyfwmatch/ ./vyfwmatch/

RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /wheels .

# Stage 3: Runtime
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

# Copy built binaries from binary-builder stage
COPY --from=binary-builder /build/ipaddrcheck/src/ipaddrcheck /usr/local/bin/ipaddrcheck

# Copy vyos-1x source tree needed by vyos_utils direct imports
COPY vyos-1x/ /opt/vyos-1x/

# Copy Python wheels and install
COPY --from=wheel-builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

RUN mkdir -p /config && chown vyfwmatch:vyfwmatch /config

USER vyfwmatch
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VYOS_1X_PATH=/opt/vyos-1x/python

VOLUME ["/config"]

# Default command shows help
ENTRYPOINT ["vyfwmatch"]
CMD ["--help"]
