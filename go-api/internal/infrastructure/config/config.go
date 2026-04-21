package config

import (
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

// Config 是 Go API 的运行配置。
type Config struct {
	AppEnv             string
	AppName            string
	GRPCAddr           string
	PythonAgentBaseURL string
	MySQLDSN           string
	RedisAddr          string
	RedisPassword      string
	RedisDB            int
}

func Load() (*Config, error) {
	// 本地开发时从 .env 加载；如果线上用容器注入环境变量，也不会受影响。
	_ = godotenv.Load()

	return &Config{
		AppEnv:             getEnv("APP_ENV", "development"),
		AppName:            getEnv("APP_NAME", "mobile-architect-api"),
		GRPCAddr:           getEnv("GRPC_ADDR", ":50051"),
		PythonAgentBaseURL: getEnv("PYTHON_AGENT_BASE_URL", "http://127.0.0.1:8080"),
		MySQLDSN:           getEnv("MYSQL_DSN", ""),
		RedisAddr:          getEnv("REDIS_ADDR", "127.0.0.1:6379"),
		RedisPassword:      getEnv("REDIS_PASSWORD", ""),
		RedisDB:            getIntEnv("REDIS_DB", 0),
	}, nil
}

func getEnv(key string, fallback string) string {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	return value
}

func getIntEnv(key string, fallback int) int {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}

	parsed, err := strconv.Atoi(value)
	if err != nil {
		return fallback
	}
	return parsed
}
