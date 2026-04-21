package main

import (
	"context"
	"log"

	"github.com/zhuanz/llm/go-api/internal/application/service"
	"github.com/zhuanz/llm/go-api/internal/infrastructure/agent"
	"github.com/zhuanz/llm/go-api/internal/infrastructure/config"
	infraMysql "github.com/zhuanz/llm/go-api/internal/infrastructure/mysql"
	infraRedis "github.com/zhuanz/llm/go-api/internal/infrastructure/redis"
	grpcserver "github.com/zhuanz/llm/go-api/internal/interfaces/grpc"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("加载配置失败: %v", err)
	}

	db, err := infraMysql.New(cfg.MySQLDSN)
	if err != nil {
		log.Fatalf("连接 MySQL 失败: %v", err)
	}

	chatRepository := infraMysql.NewChatRepository(db)
	if err := chatRepository.AutoMigrate(); err != nil {
		log.Fatalf("执行 MySQL 迁移失败: %v", err)
	}

	redisClient := infraRedis.New(cfg.RedisAddr, cfg.RedisPassword, cfg.RedisDB)
	if err := redisClient.Ping(context.Background()).Err(); err != nil {
		log.Fatalf("连接 Redis 失败: %v", err)
	}

	cache := infraRedis.NewCache(redisClient)
	agentClient := agent.NewHTTPClient(cfg.PythonAgentBaseURL)

	appService := service.NewMobileArchitectService(agentClient, cache, chatRepository)
	handler := grpcserver.NewMobileArchitectHandler(appService)
	server := grpcserver.NewServer(handler)

	listener, err := grpcserver.Listen(cfg.GRPCAddr)
	if err != nil {
		log.Fatalf("监听 gRPC 地址失败: %v", err)
	}

	log.Printf("gRPC 服务启动成功，监听地址: %s", cfg.GRPCAddr)
	if err := server.Serve(listener); err != nil {
		log.Fatalf("gRPC 服务运行失败: %v", err)
	}
}
