package mysql

import (
	"context"
	"encoding/json"
	"time"

	"github.com/zhuanz/llm/go-api/internal/domain/chat"
	"gorm.io/gorm"
)

type conversationModel struct {
	ID                         uint64    `gorm:"primaryKey;autoIncrement"`
	ThreadID                   string    `gorm:"size:128;index"`
	UserName                   string    `gorm:"size:64"`
	TargetPlatform             string    `gorm:"size:32"`
	ExperienceLevel            string    `gorm:"size:32"`
	PreferredLanguage          string    `gorm:"size:32"`
	Question                   string    `gorm:"type:text"`
	Summary                    string    `gorm:"type:text"`
	ArchitectureRecommendation string    `gorm:"type:text"`
	PerformanceRecommendation  string    `gorm:"type:text"`
	DesignPrinciples           string    `gorm:"type:text"`
	RisksJSON                  string    `gorm:"column:risks_json;type:json"`
	LearningNotesJSON          string    `gorm:"column:learning_notes_json;type:json"`
	CreatedAt                  time.Time `gorm:"autoCreateTime"`
}

func (conversationModel) TableName() string {
	return "conversations"
}

type ChatRepository struct {
	db *gorm.DB
}

func NewChatRepository(db *gorm.DB) *ChatRepository {
	return &ChatRepository{db: db}
}

func (r *ChatRepository) AutoMigrate() error {
	return r.db.AutoMigrate(&conversationModel{})
}

func (r *ChatRepository) Save(ctx context.Context, conversation *chat.Conversation) error {
	risksJSON, err := json.Marshal(conversation.Risks)
	if err != nil {
		return err
	}

	learningNotesJSON, err := json.Marshal(conversation.LearningNotes)
	if err != nil {
		return err
	}

	model := conversationModel{
		ThreadID:                   conversation.ThreadID,
		UserName:                   conversation.UserName,
		TargetPlatform:             conversation.TargetPlatform,
		ExperienceLevel:            conversation.ExperienceLevel,
		PreferredLanguage:          conversation.PreferredLanguage,
		Question:                   conversation.Question,
		Summary:                    conversation.Summary,
		ArchitectureRecommendation: conversation.ArchitectureRecommendation,
		PerformanceRecommendation:  conversation.PerformanceRecommendation,
		DesignPrinciples:           conversation.DesignPrinciples,
		RisksJSON:                  string(risksJSON),
		LearningNotesJSON:          string(learningNotesJSON),
	}

	return r.db.WithContext(ctx).Create(&model).Error
}
