package redis

import (
	"context"
	"encoding/json"
	"errors"
	"time"

	goredis "github.com/go-redis/redis/v8"
	"github.com/zhuanz/llm/go-api/internal/application/dto"
)

type Cache struct {
	client *goredis.Client
}

func NewCache(client *goredis.Client) *Cache {
	return &Cache{client: client}
}

func (c *Cache) GetExpertAnswer(ctx context.Context, key string) (*dto.ExpertAnswer, error) {
	value, err := c.client.Get(ctx, key).Result()
	if err != nil {
		if errors.Is(err, goredis.Nil) {
			return nil, nil
		}
		return nil, err
	}

	var answer dto.ExpertAnswer
	if err := json.Unmarshal([]byte(value), &answer); err != nil {
		return nil, err
	}
	return &answer, nil
}

func (c *Cache) SetExpertAnswer(
	ctx context.Context,
	key string,
	value *dto.ExpertAnswer,
	ttl time.Duration,
) error {
	data, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return c.client.Set(ctx, key, data, ttl).Err()
}
