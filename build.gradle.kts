plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.compose.compiler) apply false
}

val djinniOutput = layout.buildDirectory.dir("generated/djinni")

tasks.register<Exec>("generateDjinni") {
    group = "code generation"
    description = "Gera Java, JNI e C++ a partir do contrato Djinni de exemplo."

    val inputFile = layout.projectDirectory.file("projeto/djinni/native_api.djinni")
    inputs.file(inputFile)
    outputs.dir(djinniOutput)

    doFirst {
        djinniOutput.get().asFile.mkdirs()
    }

    commandLine(
        layout.projectDirectory.file("tools/generate-djinni.sh").asFile.absolutePath,
        inputFile.asFile.absolutePath,
        djinniOutput.get().asFile.absolutePath,
    )
}

