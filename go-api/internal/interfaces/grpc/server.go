package grpc

import (
	"net"

	mobilearchitectv1 "github.com/zhuanz/llm/go-api/gen/proto/mobile_architect/v1"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

func NewServer(handler *MobileArchitectHandler) *grpc.Server {
	server := grpc.NewServer()
	mobilearchitectv1.RegisterMobileArchitectServiceServer(server, handler)

	// 开发期打开 reflection，便于用 grpcurl / BloomRPC / Postman 调试。
	reflection.Register(server)
	return server
}

func Listen(address string) (net.Listener, error) {
	return net.Listen("tcp", address)
}
