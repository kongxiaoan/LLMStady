package com.tcm.llmclient.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.tcm.llmclient.data.AskExpertRequest
import com.tcm.llmclient.network.NetworkService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class DemoUiState(
    val isBusy: Boolean = false,
    val health: String? = null,
    val answer: String? = null,
    val error: String? = null
)

class DemoViewModel : ViewModel() {

    private val api = NetworkService.mobileArchitectApi

    private val _uiState = MutableStateFlow(DemoUiState())
    val uiState: StateFlow<DemoUiState> = _uiState.asStateFlow()

    init {
        refreshHealth()
    }

    fun refreshHealth() {
        viewModelScope.launch {
            _uiState.update { it.copy(isBusy = true, error = null) }
            runCatching { api.healthz() }
                .onSuccess { res ->
                    _uiState.update {
                        it.copy(
                            isBusy = false,
                            health = res.status
                        )
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(
                            isBusy = false,
                            health = null,
                            error = e.message ?: e.toString()
                        )
                    }
                }
        }
    }

    fun ask(question: String) {
        val q = question.trim()
        if (q.isEmpty()) {
            _uiState.update { it.copy(error = "请输入问题。") }
            return
        }
        viewModelScope.launch {
            _uiState.update { it.copy(isBusy = true, error = null) }
            runCatching {
                api.ask(
                    AskExpertRequest(
                        question = q,
                        threadId = "android-demo"
                    )
                )
            }
                .onSuccess { r ->
                    val text = buildString {
                        appendLine("【摘要】\n${r.summary}\n")
                        appendLine("【架构】\n${r.architectureRecommendation}\n")
                        appendLine("【性能】\n${r.performanceRecommendation}\n")
                        appendLine("【设计原则】\n${r.designPrinciples}\n")
                        if (r.risks.isNotEmpty()) {
                            appendLine("【风险】")
                            r.risks.forEach { appendLine("- $it") }
                            appendLine()
                        }
                        if (r.learningNotes.isNotEmpty()) {
                            appendLine("【延伸】")
                            r.learningNotes.forEach { appendLine("- $it") }
                        }
                    }
                    _uiState.update { it.copy(isBusy = false, answer = text, error = null) }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(
                            isBusy = false,
                            error = e.message ?: e.toString()
                        )
                    }
                }
        }
    }
}
