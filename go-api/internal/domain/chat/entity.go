package chat

import "time"

// Conversation 代表一轮完整的业务问答记录。
// 在 DDD 里，它属于领域实体，负责描述“什么是会话记录”。
type Conversation struct {
	ID                         uint64
	ThreadID                   string
	UserName                   string
	TargetPlatform             string
	ExperienceLevel            string
	PreferredLanguage          string
	Question                   string
	Summary                    string
	ArchitectureRecommendation string
	PerformanceRecommendation  string
	DesignPrinciples           string
	Risks                      []string
	LearningNotes              []string
	CreatedAt                  time.Time
}
