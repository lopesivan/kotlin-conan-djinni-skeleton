import org.gradle.api.DefaultTask
import org.gradle.api.file.DirectoryProperty
import org.gradle.api.file.RegularFileProperty
import org.gradle.api.tasks.InputFile
import org.gradle.api.tasks.OutputDirectory
import org.gradle.api.tasks.PathSensitive
import org.gradle.api.tasks.PathSensitivity
import org.gradle.api.tasks.TaskAction
import org.gradle.process.ExecOperations
import org.gradle.work.DisableCachingByDefault
import javax.inject.Inject

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.compose.compiler)
}

@DisableCachingByDefault(because = "Executa o gerador Djinni externo")
abstract class GenerateDjinniTask @Inject constructor(
    private val execOperations: ExecOperations,
) : DefaultTask() {

    @get:InputFile
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val scriptFile: RegularFileProperty

    @get:InputFile
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val contractFile: RegularFileProperty

    @get:InputFile
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val conanRecipeFile: RegularFileProperty

    @get:OutputDirectory
    abstract val javaOutputDirectory: DirectoryProperty

    @get:OutputDirectory
    abstract val cppOutputDirectory: DirectoryProperty

    @get:OutputDirectory
    abstract val jniOutputDirectory: DirectoryProperty

    @get:OutputDirectory
    abstract val conanOutputDirectory: DirectoryProperty

    @get:OutputDirectory
    abstract val supportOutputDirectory: DirectoryProperty

    @TaskAction
    fun generate() {
        execOperations.exec {
            commandLine(scriptFile.get().asFile.absolutePath)
        }
    }
}

val requestedAbis = (findProperty("projectAbis") as String? ?: "arm64-v8a")
    .split(',')
    .map(String::trim)
    .filter(String::isNotEmpty)

val generateDjinni = tasks.register<GenerateDjinniTask>("generateDjinni") {
    group = "code generation"
    description = "Gera Java, JNI e C++ para o contrato native_api.djinni."

    scriptFile.set(layout.projectDirectory.file("generate-djinni.sh"))
    contractFile.set(
        rootProject.layout.projectDirectory.file("projeto/djinni/native_api.djinni"),
    )
    conanRecipeFile.set(layout.projectDirectory.file("conanfile.txt"))
    javaOutputDirectory.set(layout.buildDirectory.dir("generated/djinni/java"))
    cppOutputDirectory.set(layout.buildDirectory.dir("generated/djinni/cpp"))
    jniOutputDirectory.set(layout.buildDirectory.dir("generated/djinni/jni"))
    conanOutputDirectory.set(layout.buildDirectory.dir("conan/djinni-generator"))
    supportOutputDirectory.set(layout.buildDirectory.dir("djinni-support-lib"))
}

android {
    namespace = "br.eng.ivanlopes.projeto01"
    compileSdk = libs.versions.compileSdk.get().toInt()
    ndkVersion = libs.versions.ndk.get()

    defaultConfig {
        applicationId = "br.eng.ivanlopes.projeto01"
        minSdk = libs.versions.minSdk.get().toInt()
        targetSdk = libs.versions.targetSdk.get().toInt()
        versionCode = 1
        versionName = "0.1.0"

        ndk {
            abiFilters.clear()
            abiFilters += requestedAbis
        }

        externalNativeBuild {
            cmake {
                cppFlags += "-std=c++20"
            }
        }
    }

    buildFeatures {
        compose = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlin {
        compilerOptions {
            jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = libs.versions.cmake.get()
        }
    }
}

androidComponents {
    onVariants(selector().all()) { variant ->
        variant.sources.java?.addGeneratedSourceDirectory(
            generateDjinni,
            GenerateDjinniTask::javaOutputDirectory,
        )
    }
}

tasks.configureEach {
    if (
        name.startsWith("configureCMake") ||
        name.startsWith("buildCMake") ||
        name.startsWith("externalNativeBuild")
    ) {
        dependsOn(generateDjinni)
    }
}

dependencies {
    implementation(platform(libs.compose.bom))
    implementation(libs.activity.compose)
    implementation(libs.compose.ui)
    implementation(libs.compose.foundation)
    implementation(libs.compose.material3)
    implementation(libs.core.ktx)
}
