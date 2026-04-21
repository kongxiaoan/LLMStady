package grpc

import (
	"context"

	mobilearchitectv1 "github.com/zhuanz/llm/go-api/gen/proto/mobile_architect/v1"
	"github.com/zhuanz/llm/go-api/internal/application/dto"
	"github.com/zhuanz/llm/go-api/internal/application/service"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type MobileArchitectHandler struct {
	mobilearchitectv1.UnimplementedMobileArchitectServiceServer
	service *service.MobileArchitectService
}

func NewMobileArchitectHandler(
	service *service.MobileArchitectService,
) *MobileArchitectHandler {
	return &MobileArchitectHandler{service: service}
}

func (h *MobileArchitectHandler) AskExpert(
	ctx context.Context,
	request *mobilearchitectv1.AskExpertRequest,
) (*mobilearchitectv1.AskExpertResponse, error) {
	if request.GetQuestion() == "" {
		return nil, status.Error(codes.InvalidArgument, "question 不能为空")
	}

	answer, err := h.service.AskExpert(ctx, dto.AskExpertCommand{
		Question:          request.GetQuestion(),
		ThreadID:          request.GetThreadId(),
		UserName:          request.GetUserName(),
		TargetPlatform:    request.GetTargetPlatform(),
		ExperienceLevel:   request.GetExperienceLevel(),
		PreferredLanguage: request.GetPreferredLanguage(),
	})
	if err != nil {
		return nil, status.Errorf(codes.Internal, "调用专家服务失败: %v", err)
	}

	return &mobilearchitectv1.AskExpertResponse{
		Summary:                    answer.Summary,
		ArchitectureRecommendation: answer.ArchitectureRecommendation,
		PerformanceRecommendation:  answer.PerformanceRecommendation,
		DesignPrinciples:           answer.DesignPrinciples,
		Risks:                      answer.Risks,
		LearningNotes:              answer.LearningNotes,
	}, nil
}
