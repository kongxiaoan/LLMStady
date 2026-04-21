package outbound

import (
	"context"
	"time"

	"github.com/zhuanz/llm/go-api/internal/application/dto"
)

// Cache 抽象了 Redis 这样的缓存能力。
type Cache interface {
	GetExpertAnswer(ctx context.Context, key string) (*dto.ExpertAnswer, error)
	SetExpertAnswer(ctx context.Context, key string, value *dto.ExpertAnswer, ttl time.Duration) error
}
