package br.eng.ivanlopes.projeto01

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import br.eng.ivanlopes.projeto01.generated.NativeApi

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { ProjectScreen() }
    }
}

private object NativeBridge {
    init {
        System.loadLibrary("project01_native")
    }

    fun message(): String = NativeApi.helloFromCpp()
}

@Composable
private fun ProjectScreen() {
    val nativeMessage = remember {
        runCatching(NativeBridge::message)
            .getOrElse { error -> "Falha ao chamar C++: ${error.message}" }
    }

    MaterialTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
            Column(
                modifier = Modifier.padding(24.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Text(
                    text = "Projeto 01",
                    style = MaterialTheme.typography.headlineMedium,
                )
                Text(
                    text = nativeMessage,
                    modifier = Modifier.padding(top = 12.dp),
                )
            }
        }
    }
}
