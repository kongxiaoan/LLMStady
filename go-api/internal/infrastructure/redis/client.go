package redis

import (
	"github.com/go-redis/redis/v8"
)

func New(addr string, password string, db int) *redis.Client {
	return redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: password,
		DB:       db,
	})
}
