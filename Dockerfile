FROM alpine:3.21.2

# This argument is defined automatically by buildx when using --platform
ARG TARGETARCH

RUN apk add --no-cache curl

ENV SH_VERSION=v0.6.10

RUN echo "TARGETARCH: ${TARGETARCH}" && \
    if [ "${TARGETARCH}" = "amd64" ]; then \
        export TARGET="x86_64-unknown-linux-musl-simple-http-server" ; \
    elif [ "${TARGETARCH}" = "arm" ]; then \
        export TARGET="armv7-unknown-linux-musleabihf-simple-http-server" ; \
    elif [ "${TARGETARCH}" = "arm64" ]; then \
        export TARGET="aarch64-unknown-linux-musl-simple-http-server" ; \
    else \
        echo "Unsupported TARGETARCH: ${TARGETARCH}" >&2; \
        exit 1; \
    fi && \
    curl -L "https://github.com/TheWaWaR/simple-http-server/releases/download/${SH_VERSION}/${TARGET}" -o "/usr/bin/simple-http-server" && \
    chmod +x /usr/bin/simple-http-server

RUN mkdir -p /docs
COPY register_service /register_service
COPY docs/BlueOS-stable/index.html /index.html

COPY docs /docs
WORKDIR /

LABEL version="2025.2.7"
LABEL permissions='{\
  "ExposedPorts": {\
    "80/tcp": {}\
  },\
  "HostConfig": {\
    "PortBindings": {\
      "80/tcp": [\
        {\
          "HostPort": ""\
        }\
      ]\
    }\
  }\
}'
LABEL authors='[\
    {\
        "name": "Patrick José Pereira",\
        "email": "patrickelectric@gmail.com"\
    },\
    {\
        "name": "ES-Alexander",\
        "email": "sandman.esalexander@gmail.com"\
    }\
]'
LABEL company='{\
    "about": "",\
    "name": "Blue Robotics",\
    "email": "support@bluerobotics.com"\
}'
LABEL type="documentation"
LABEL readme="https://raw.githubusercontent.com/bluerobotics/BlueRobotics-docs-Extension/master/README.md"
LABEL type="other"
LABEL tags='[\
  "development",\
  "documentation",\
]'

CMD ["simple-http-server", "-p", "80", "-i"]
