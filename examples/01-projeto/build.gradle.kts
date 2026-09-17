import org.gradle.api.tasks.Exec

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.compose.compiler)
}

val requestedAbis = (findProperty("projectAbis") as String? ?: "arm64-v8a")
    .split(',')
    .map(String::trim)
    .filter(String::isNotEmpty)

val djinniOutput = layout.buildDirectory.dir("generated/djinni")
val djinniJava = djinniOutput.map { it.dir("java") }

val generateDjinni by tasks.registering(Exec::class) {
    group = "code generation"
    description = "Gera Java, JNI e C++ para o contrato native_api.djinni."

    val script = layout.projectDirectory.file("generate-djinni.sh")
    val contract = rootProject.layout.projectDirectory.file("projeto/djinni/native_api.djinni")

    inputs.file(script)
    inputs.file(contract)
    outputs.dir(djinniOutput)

    commandLine(script.asFile.absolutePath)
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

    sourceSets {
        named("main") {
            java.srcDir(djinniJava)
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = libs.versions.cmake.get()
        }
    }
}

tasks.configureEach {
    if (
        name == "preBuild" ||
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
