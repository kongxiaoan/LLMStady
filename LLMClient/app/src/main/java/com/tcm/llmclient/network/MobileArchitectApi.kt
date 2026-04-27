package com.tcm.llmclient.network

import com.tcm.llmclient.data.AskExpertRequest
import com.tcm.llmclient.data.AskExpertResponse
import com.tcm.llmclient.data.HealthzResponse
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

/** 与 Python llm http 层 JSON 一致，字段与 go-api 的 proto 对齐。 */
interface MobileArchitectApi {

    @GET("healthz")
    suspend fun healthz(): HealthzResponse

    @POST("v1/mobile-architect/ask")
    suspend fun ask(@Body request: AskExpertRequest): AskExpertResponse
}
