ARG IMG_TAG=latest
ARG local_build

FROM alpine:$IMG_TAG
RUN apk add --no-cache git
RUN apk add --no-cache make
COPY --from=golang:1.22.10-alpine /usr/local/go/ /usr/local/go/

ENV GOPATH="/usr/local/go"
ENV PATH="${GOPATH}/bin:${PATH}"
#RUN git clone https://github.com/atomone-hub/atomone.git
COPY ./atomone /atomone
WORKDIR "/atomone"
RUN make build
RUN cp /atomone/build/atomoned /bin

EXPOSE 26656 26657 1317 9090
#ENTRYPOINT ["/atomone/build/atomoned", "start"]



