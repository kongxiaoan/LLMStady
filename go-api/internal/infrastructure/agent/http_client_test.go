package agent

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/zhuanz/llm/go-api/internal/application/dto"
)

func TestHTTPClientAskExpert(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1/mobile-architect/ask" {
			t.Fatalf("unexpected path: %s", r.URL.Path)
		}

		if r.Method != http.MethodPost {
			t.Fatalf("unexpected method: %s", r.Method)
		}

		var requestBody map[string]any
		if err := json.NewDecoder(r.Body).Decode(&requestBody); err != nil {
			t.Fatalf("decode request failed: %v", err)
		}

		if requestBody["question"] != "如何优化 Android 启动" {
			t.Fatalf("unexpected question: %v", requestBody["question"])
		}

		_ = json.NewEncoder(w).Encode(map[string]any{
			"summary":                     "先建立启动链路观测",
			"architecture_recommendation": "拆分首页初始化职责",
			"performance_recommendation":  "缩短主线程关键路径",
			"design_principles":           "单一职责 + 依赖倒置",
			"risks":                       []string{"过早抽象"},
			"learning_notes":              []string{"先测量再优化"},
		})
	}))
	defer server.Close()

	client := NewHTTPClient(server.URL)
	answer, err := client.AskExpert(context.Background(), dto.AskExpertCommand{
		Question:          "如何优化 Android 启动",
		ThreadID:          "thread-1",
		UserName:          "Zhuanz",
		TargetPlatform:    "android",
		ExperienceLevel:   "intermediate",
		PreferredLanguage: "java",
	})
	if err != nil {
		t.Fatalf("AskExpert failed: %v", err)
	}

	if answer.Summary != "先建立启动链路观测" {
		t.Fatalf("unexpected summary: %s", answer.Summary)
	}
}
