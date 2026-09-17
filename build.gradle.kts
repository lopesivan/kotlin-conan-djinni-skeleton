plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.compose.compiler) apply false
}

tasks.register("generateDjinni") {
    group = "code generation"
    description = "Gera a fronteira Djinni usada pelo Projeto 01."
    dependsOn(":examples:01-projeto:generateDjinni")
}
