package com.tcm.llmclient

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.tcm.llmclient.ui.DemoViewModel
import com.tcm.llmclient.ui.theme.LLMClientTheme

class MainActivity : ComponentActivity() {
    @OptIn(ExperimentalMaterial3Api::class)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val viewModel: DemoViewModel = viewModel()
            val state by viewModel.uiState.collectAsStateWithLifecycle()
            val snackbar = remember { SnackbarHostState() }
            LaunchedEffect(state.error) {
                val msg = state.error
                if (msg != null) {
                    snackbar.showSnackbar(msg)
                }
            }
            LLMClientTheme {
                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    topBar = {
                        TopAppBar(
                            title = { Text("LLM Client 联调") }
                        )
                    },
                    snackbarHost = { SnackbarHost(hostState = snackbar) }
                ) { padding ->
                    Column(
                        modifier = Modifier
                            .padding(padding)
                            .padding(16.dp)
                            .fillMaxSize()
                            .verticalScroll(rememberScrollState())
                    ) {
                        state.health?.let { h ->
                            Text(
                                "健康检查: $h",
                                style = MaterialTheme.typography.bodyLarge
                            )
                        }
                        if (state.isBusy) {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 8.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                CircularProgressIndicator()
                            }
                        }
                        DemoQuestionForm(
                            isBusy = state.isBusy,
                            onCheckHealth = { viewModel.refreshHealth() },
                            onSubmit = { viewModel.ask(it) }
                        )
                        if (state.answer != null) {
                            Text(
                                "回答",
                                style = MaterialTheme.typography.titleMedium,
                                modifier = Modifier.padding(top = 16.dp)
                            )
                            Text(
                                state.answer!!,
                                style = MaterialTheme.typography.bodyMedium
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun DemoQuestionForm(
    isBusy: Boolean,
    onCheckHealth: () -> Unit,
    onSubmit: (String) -> Unit
) {
    var text by remember {
        mutableStateOf("请用要点说明 Android 大型项目的分层架构与模块边界。")
    }
    Column(
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        OutlinedTextField(
            value = text,
            onValueChange = { text = it },
            label = { Text("问题") },
            minLines = 3,
            modifier = Modifier.fillMaxWidth(),
            enabled = !isBusy
        )
        Button(
            onClick = onCheckHealth,
            enabled = !isBusy,
            modifier = Modifier.fillMaxWidth()
        ) { Text("重试 /healthz") }
        Button(
            onClick = { onSubmit(text) },
            enabled = !isBusy,
            modifier = Modifier.fillMaxWidth()
        ) { Text("向 Agent 提问") }
    }
}
