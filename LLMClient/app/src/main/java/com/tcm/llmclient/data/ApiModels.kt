package com.tcm.llmclient.data

import com.google.gson.annotations.SerializedName

data class HealthzResponse(
    @SerializedName("status")
    val status: String
)

data class AskExpertRequest(
    @SerializedName("question")
    val question: String,
    @SerializedName("thread_id")
    val threadId: String? = null,
    @SerializedName("user_name")
    val userName: String = "AndroidClient",
    @SerializedName("target_platform")
    val targetPlatform: String = "android",
    @SerializedName("experience_level")
    val experienceLevel: String = "intermediate",
    @SerializedName("preferred_language")
    val preferredLanguage: String = "kotlin"
)

data class AskExpertResponse(
    @SerializedName("summary")
    val summary: String,
    @SerializedName("architecture_recommendation")
    val architectureRecommendation: String,
    @SerializedName("performance_recommendation")
    val performanceRecommendation: String,
    @SerializedName("design_principles")
    val designPrinciples: String,
    @SerializedName("risks")
    val risks: List<String>,
    @SerializedName("learning_notes")
    val learningNotes: List<String>
)
