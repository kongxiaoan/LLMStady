package agent

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	"github.com/zhuanz/llm/go-api/internal/application/dto"
)

type HTTPClient struct {
	baseURL    string
	httpClient *http.Client
}

type askExpertRequest struct {
	Question          string `json:"question"`
	ThreadID          string `json:"thread_id"`
	UserName          string `json:"user_name"`
	TargetPlatform    string `json:"target_platform"`
	ExperienceLevel   string `json:"experience_level"`
	PreferredLanguage string `json:"preferred_language"`
}

type askExpertResponse struct {
	Summary                    string   `json:"summary"`
	ArchitectureRecommendation string   `json:"architecture_recommendation"`
	PerformanceRecommendation  string   `json:"performance_recommendation"`
	DesignPrinciples           string   `json:"design_principles"`
	Risks                      []string `json:"risks"`
	LearningNotes              []string `json:"learning_notes"`
}

func NewHTTPClient(baseURL string) *HTTPClient {
	return &HTTPClient{
		baseURL: strings.TrimRight(baseURL, "/"),
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

func (c *HTTPClient) AskExpert(
	ctx context.Context,
	command dto.AskExpertCommand,
) (*dto.ExpertAnswer, error) {
	payload := askExpertRequest{
		Question:          command.Question,
		ThreadID:          command.ThreadID,
		UserName:          command.UserName,
		TargetPlatform:    command.TargetPlatform,
		ExperienceLevel:   command.ExperienceLevel,
		PreferredLanguage: command.PreferredLanguage,
	}

	body, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	request, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		c.baseURL+"/v1/mobile-architect/ask",
		bytes.NewReader(body),
	)
	if err != nil {
		return nil, err
	}
	request.Header.Set("Content-Type", "application/json")

	response, err := c.httpClient.Do(request)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode >= http.StatusBadRequest {
		rawBody, _ := io.ReadAll(response.Body)
		return nil, fmt.Errorf("python agent 返回错误: status=%d body=%s", response.StatusCode, string(rawBody))
	}

	var result askExpertResponse
	if err := json.NewDecoder(response.Body).Decode(&result); err != nil {
		return nil, err
	}

	return &dto.ExpertAnswer{
		Summary:                    result.Summary,
		ArchitectureRecommendation: result.ArchitectureRecommendation,
		PerformanceRecommendation:  result.PerformanceRecommendation,
		DesignPrinciples:           result.DesignPrinciples,
		Risks:                      result.Risks,
		LearningNotes:              result.LearningNotes,
	}, nil
}
