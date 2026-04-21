package service

import (
	"context"
	"testing"
	"time"

	"github.com/zhuanz/llm/go-api/internal/application/dto"
	"github.com/zhuanz/llm/go-api/internal/domain/chat"
)

type fakeAgentClient struct{}

func (f *fakeAgentClient) AskExpert(ctx context.Context, command dto.AskExpertCommand) (*dto.ExpertAnswer, error) {
	return &dto.ExpertAnswer{
		Summary:                    "回答摘要",
		ArchitectureRecommendation: "架构建议",
		PerformanceRecommendation:  "性能建议",
		DesignPrinciples:           "设计原则",
		Risks:                      []string{"风险A"},
		LearningNotes:              []string{"要点A"},
	}, nil
}

type fakeCache struct {
	value *dto.ExpertAnswer
}

func (f *fakeCache) GetExpertAnswer(ctx context.Context, key string) (*dto.ExpertAnswer, error) {
	return f.value, nil
}

func (f *fakeCache) SetExpertAnswer(ctx context.Context, key string, value *dto.ExpertAnswer, ttl time.Duration) error {
	f.value = value
	return nil
}

type fakeRepository struct {
	saved bool
}

func (f *fakeRepository) Save(ctx context.Context, conversation *chat.Conversation) error {
	f.saved = true
	return nil
}

func TestAskExpertUsesAgentAndPersists(t *testing.T) {
	cache := &fakeCache{}
	repository := &fakeRepository{}
	service := NewMobileArchitectService(&fakeAgentClient{}, cache, repository)

	answer, err := service.AskExpert(context.Background(), dto.AskExpertCommand{
		Question:          "如何做架构设计",
		ThreadID:          "thread-1",
		UserName:          "Zhuanz",
		TargetPlatform:    "android",
		ExperienceLevel:   "intermediate",
		PreferredLanguage: "java",
	})
	if err != nil {
		t.Fatalf("AskExpert failed: %v", err)
	}

	if answer.Summary != "回答摘要" {
		t.Fatalf("unexpected summary: %s", answer.Summary)
	}

	if !repository.saved {
		t.Fatal("expected conversation to be persisted")
	}
}

func TestAskExpertUsesCacheFirst(t *testing.T) {
	cache := &fakeCache{
		value: &dto.ExpertAnswer{Summary: "缓存命中"},
	}
	repository := &fakeRepository{}
	service := NewMobileArchitectService(&fakeAgentClient{}, cache, repository)

	answer, err := service.AskExpert(context.Background(), dto.AskExpertCommand{
		Question: "重复问题",
	})
	if err != nil {
		t.Fatalf("AskExpert failed: %v", err)
	}

	if answer.Summary != "缓存命中" {
		t.Fatalf("unexpected summary: %s", answer.Summary)
	}

	if repository.saved {
		t.Fatal("cache hit should not persist conversation again")
	}
}
