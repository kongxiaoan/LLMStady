PROTO_DIR=proto
PROTO_OUT=gen/proto

.PHONY: proto run tidy test

proto:
	PATH="$(PATH):$(HOME)/go/bin" protoc \
		-I $(PROTO_DIR) \
		--go_out=$(PROTO_OUT) --go_opt=paths=source_relative \
		--go-grpc_out=$(PROTO_OUT) --go-grpc_opt=paths=source_relative \
		$(PROTO_DIR)/mobile_architect/v1/mobile_architect.proto

run:
	go run ./cmd/server

tidy:
	go mod tidy

test:
	go test ./...
