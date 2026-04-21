package outbound

import (
	"context"

	"github.com/zhuanz/llm/go-api/internal/application/dto"
)

// AgentClient 抽象了“如何调用 Python Agent”。
// 这样应用层不依赖具体协议，可以是 HTTP、gRPC、消息队列等。
type AgentClient interface {
	AskExpert(ctx context.Context, command dto.AskExpertCommand) (*dto.ExpertAnswer, error)
}
