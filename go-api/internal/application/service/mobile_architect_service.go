package service

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"strings"
	"time"

	"github.com/zhuanz/llm/go-api/internal/application/dto"
	"github.com/zhuanz/llm/go-api/internal/application/port/outbound"
	"github.com/zhuanz/llm/go-api/internal/domain/chat"
)

// MobileArchitectService 是应用服务。
// 这层负责编排用例，而不是承载底层技术细节。
type MobileArchitectService struct {
	agentClient outbound.AgentClient
	cache       outbound.Cache
	repository  chat.Repository
}

func NewMobileArchitectService(
	agentClient outbound.AgentClient,
	cache outbound.Cache,
	repository chat.Repository,
) *MobileArchitectService {
	return &MobileArchitectService{
		agentClient: agentClient,
		cache:       cache,
		repository:  repository,
	}
}

func (s *MobileArchitectService) AskExpert(
	ctx context.Context,
	command dto.AskExpertCommand,
) (*dto.ExpertAnswer, error) {
	cacheKey := buildCacheKey(command)

	// 先查 Redis，减少重复问题对模型与 Python Agent 的压力。
	if cached, err := s.cache.GetExpertAnswer(ctx, cacheKey); err == nil && cached != nil {
		return cached, nil
	}

	answer, err := s.agentClient.AskExpert(ctx, command)
	if err != nil {
		return nil, err
	}

	conversation := &chat.Conversation{
		ThreadID:                   command.ThreadID,
		UserName:                   command.UserName,
		TargetPlatform:             command.TargetPlatform,
		ExperienceLevel:            command.ExperienceLevel,
		PreferredLanguage:          command.PreferredLanguage,
		Question:                   command.Question,
		Summary:                    answer.Summary,
		ArchitectureRecommendation: answer.ArchitectureRecommendation,
		PerformanceRecommendation:  answer.PerformanceRecommendation,
		DesignPrinciples:           answer.DesignPrinciples,
		Risks:                      answer.Risks,
		LearningNotes:              answer.LearningNotes,
	}

	if err := s.repository.Save(ctx, conversation); err != nil {
		return nil, err
	}

	_ = s.cache.SetExpertAnswer(ctx, cacheKey, answer, 10*time.Minute)

	return answer, nil
}

func buildCacheKey(command dto.AskExpertCommand) string {
	normalized := strings.Join(
		[]string{
			command.Question,
			command.ThreadID,
			command.TargetPlatform,
			command.ExperienceLevel,
			command.PreferredLanguage,
		},
		"|",
	)
	sum := sha256.Sum256([]byte(normalized))
	return "mobile_architect:" + hex.EncodeToString(sum[:])
}
