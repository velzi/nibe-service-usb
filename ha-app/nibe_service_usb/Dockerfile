FROM ghcr.io/astral-sh/uv:0.12.15 AS uv

FROM python:3.13-slim

# The Supervisor passes the App version from config.yaml. No default, so a
# build without it fails instead of installing a stale release.
ARG BUILD_VERSION
# Where the gateway comes from. A fork changes this line.
ARG GATEWAY_REPO=https://github.com/velzi/nibe-service-usb
# Branch or tag to install; override only for testing (e.g. main).
ARG GATEWAY_REF=v${BUILD_VERSION}

ADD ${GATEWAY_REPO}/archive/${GATEWAY_REF}.tar.gz /tmp/gateway.tar.gz

# Installs the exact dependency versions from uv.lock with the image's Python.
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    mkdir /opt/nibe-service-usb \
    && tar -xzf /tmp/gateway.tar.gz -C /opt/nibe-service-usb --strip-components=1 \
    && rm /tmp/gateway.tar.gz \
    && cd /opt/nibe-service-usb \
    && UV_PYTHON_DOWNLOADS=never uv sync --locked --no-dev --no-editable \
       --python-preference only-system --compile-bytecode --no-cache

# config.yaml maps the App's config folder here: the optional config.toml
# (the gateway's default path) plus auth.key and server_id.
ENV NIBE_SERVICE_USB_DATA_DIR=/etc/nibe-service-usb \
    PATH=/opt/nibe-service-usb/.venv/bin:$PATH

CMD ["nibe-service-usb", "run"]
