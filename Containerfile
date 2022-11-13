FROM golang:latest AS build-env

WORKDIR /src

ENV CGO_ENABLED=0

COPY go.mod /src/

RUN go mod download

COPY . .

RUN  go build -a -o mozitools

FROM alpine:latest

RUN apk add --no-cache upx \
    && rm -rf /var/cache/*

RUN mkdir -p /app \
    && adduser -D mozitools \
    && chown -R mozitools:mozitools /app

USER mozitools

WORKDIR /app

COPY --from=build-env /src/mozitools .

ENTRYPOINT [ "./mozitools" ]