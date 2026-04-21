package dto

// AskExpertCommand 是应用层命令对象。
// 它聚合了当前 use case 需要的所有输入。
type AskExpertCommand struct {
	Question          string
	ThreadID          string
	UserName          string
	TargetPlatform    string
	ExperienceLevel   string
	PreferredLanguage string
}

// ExpertAnswer 是应用层返回对象。
// 它和 Python Agent 的结构化输出字段一一对应，便于跨语言协作。
type ExpertAnswer struct {
	Summary                    string
	ArchitectureRecommendation string
	PerformanceRecommendation  string
	DesignPrinciples           string
	Risks                      []string
	LearningNotes              []string
}
