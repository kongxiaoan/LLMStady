package chat

import "context"

// Repository 是领域层对持久化能力的抽象。
// 领域层不关心底层是 MySQL、PostgreSQL 还是别的存储。
type Repository interface {
	Save(ctx context.Context, conversation *Conversation) error
}
