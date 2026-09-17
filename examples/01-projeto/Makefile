SHELL := /bin/bash

## ---------------------------------------------------------------------------
## Caminhos do projeto
## ---------------------------------------------------------------------------

MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PROJECT_DIR  := $(patsubst %/,%,$(MAKEFILE_DIR))
ROOT         := $(abspath $(PROJECT_DIR)/../..)

ANDROID_SDK    ?= /home/ivan/Android/Sdk
NDK_VERSION    := 29.0.14206865
CMAKE_VERSION  := 4.4.3
GRADLE_VERSION := 9.6.1

ANDROID_NDK_HOME := $(ANDROID_SDK)/ndk/$(NDK_VERSION)

## CMake instalado localmente
CMAKE_HOME := /home/ivan/.local
CMAKE      := $(CMAKE_HOME)/bin/cmake

## Ninja encontrado no PATH
NINJA := $(shell command -v ninja 2>/dev/null)

ADB := $(ANDROID_SDK)/platform-tools/adb

CONAN ?= conan
JAVA  ?= java
GIT   ?= git

GRADLEW            := $(ROOT)/gradlew
GRADLE_WRAPPER_DIR := $(ROOT)/gradle/wrapper
LOCAL_PROPERTIES   := $(ROOT)/local.properties
DJINNI_SCRIPT      := $(PROJECT_DIR)/generate-djinni.sh

MODULE   := :examples:01-projeto
PACKAGE  := br.eng.ivanlopes.projeto01
ACTIVITY := .MainActivity
APK      := $(PROJECT_DIR)/build/outputs/apk/debug/01-projeto-debug.apk

ABI    ?= arm64-v8a
DEVICE ?=

ADB_TARGET := $(if $(DEVICE),-s $(DEVICE),)

log = @printf "\033[36m[make]\033[0m %s\n" "$(1)"

.DEFAULT_GOAL := help

.PHONY: help init djinni build install run stop uninstall clean logcat devices

## ---------------------------------------------------------------------------
## Ajuda
## ---------------------------------------------------------------------------

help:
	@printf "make init       verifica Gradle, Conan, Java e Android SDK\n"
	@printf "make djinni     gera Java/JNI/C++ a partir do contrato\n"
	@printf "make build      gera Djinni e compila o APK debug\n"
	@printf "make install    compila e instala o APK\n"
	@printf "make run        instala e inicia o aplicativo\n"
	@printf "make logcat     mostra somente os logs do aplicativo\n"
	@printf "DEVICE=serial   seleciona um dispositivo ADB\n"

## ---------------------------------------------------------------------------
## Preparação e verificação
## ---------------------------------------------------------------------------

init:
	$(call log,$@)

	@test -d "$(ANDROID_SDK)" || \
		{ echo "Erro: SDK não encontrado em $(ANDROID_SDK)"; exit 1; }

	@test -d "$(ANDROID_NDK_HOME)" || \
		{ echo "Erro: NDK não encontrado em $(ANDROID_NDK_HOME)"; exit 1; }

	@test -x "$(ADB)" || \
		{ echo "Erro: adb não encontrado em $(ADB)"; exit 1; }

	@test -d "$(CMAKE_HOME)" || \
		{ echo "Erro: diretório do CMake não encontrado em $(CMAKE_HOME)"; exit 1; }

	@test -x "$(CMAKE)" || \
		{ echo "Erro: CMake não encontrado em $(CMAKE)"; exit 1; }

	@test -n "$(NINJA)" && test -x "$(NINJA)" || \
		{ echo "Erro: Ninja não encontrado no PATH"; exit 1; }

	@command -v "$(CONAN)" >/dev/null 2>&1 || \
		{ echo "Erro: Conan não encontrado"; exit 1; }

	@command -v "$(JAVA)" >/dev/null 2>&1 || \
		{ echo "Erro: Java não encontrado"; exit 1; }

	@command -v "$(GIT)" >/dev/null 2>&1 || \
		{ echo "Erro: Git não encontrado"; exit 1; }

	@test -f "$(GRADLEW)" || \
		{ echo "Erro: gradlew não encontrado em $(GRADLEW)"; exit 1; }

	@test -f "$(GRADLE_WRAPPER_DIR)/gradle-wrapper.jar" || \
		{ echo "Erro: gradle-wrapper.jar não encontrado"; exit 1; }

	@test -f "$(GRADLE_WRAPPER_DIR)/gradle-wrapper.properties" || \
		{ echo "Erro: gradle-wrapper.properties não encontrado"; exit 1; }

	@test -f "$(DJINNI_SCRIPT)" || \
		{ echo "Erro: generate-djinni.sh não encontrado"; exit 1; }

	@first_line="$$($(CMAKE) --version | head -n 1)"; \
		test "$$first_line" = "cmake version $(CMAKE_VERSION)" || \
		{ echo "Erro: é necessário CMake $(CMAKE_VERSION)"; \
		  echo "Encontrado: $$first_line"; exit 1; }

	@"$(CONAN)" --version | grep -Eq "^Conan version 2\." || \
		{ echo "Erro: é necessário Conan 2"; \
		  "$(CONAN)" --version; exit 1; }

	@grep -Fq "gradle-$(GRADLE_VERSION)-bin.zip" \
		"$(GRADLE_WRAPPER_DIR)/gradle-wrapper.properties" || \
		{ echo "Erro: o projeto requer Gradle $(GRADLE_VERSION)"; exit 1; }

	@chmod +x "$(GRADLEW)" "$(DJINNI_SCRIPT)"

	@tmp="$(LOCAL_PROPERTIES).tmp"; \
	{ \
		grep -Ev '^(sdk|cmake)\.dir=' \
			"$(LOCAL_PROPERTIES)" 2>/dev/null || true; \
		printf 'sdk.dir=%s\n' "$(ANDROID_SDK)"; \
		printf 'cmake.dir=%s\n' "$(CMAKE_HOME)"; \
	} > "$$tmp"; \
	mv "$$tmp" "$(LOCAL_PROPERTIES)"

	@grep -Fxq 'sdk.dir=$(ANDROID_SDK)' "$(LOCAL_PROPERTIES)" || \
		{ echo "Erro em $(LOCAL_PROPERTIES)"; \
		  echo "Esperado: sdk.dir=$(ANDROID_SDK)"; exit 1; }

	@grep -Fxq 'cmake.dir=$(CMAKE_HOME)' "$(LOCAL_PROPERTIES)" || \
		{ echo "Erro em $(LOCAL_PROPERTIES)"; \
		  echo "Esperado: cmake.dir=$(CMAKE_HOME)"; exit 1; }

	@echo
	@echo "Ambiente encontrado:"
	@echo "  Raiz   : $(ROOT)"
	@echo "  SDK    : $(ANDROID_SDK)"
	@echo "  NDK    : $(ANDROID_NDK_HOME)"
	@echo "  CMake  : $$($(CMAKE) --version | head -n 1)"
	@echo "  Ninja  : $$($(NINJA) --version)"
	@echo "  Conan  : $$($(CONAN) --version)"
	@echo "  Java   : $$($(JAVA) -version 2>&1 | head -n 1)"
	@echo "  Git    : $$($(GIT) --version)"
	@echo
	@cd "$(ROOT)" && "$(GRADLEW)" --version

## ---------------------------------------------------------------------------
## Geração de código
## ---------------------------------------------------------------------------

djinni: init
	$(call log,$@)
	@cd "$(ROOT)" && "$(GRADLEW)" $(MODULE):generateDjinni

## ---------------------------------------------------------------------------
## Compilação, instalação e execução
## ---------------------------------------------------------------------------

build: init
	$(call log,$@)
	@cd "$(ROOT)" && "$(GRADLEW)" $(MODULE):assembleDebug \
		-PprojectAbis="$(ABI)"

install: build
	$(call log,$@)
	@test -f "$(APK)" || \
		{ echo "Erro: APK não encontrado em $(APK)"; exit 1; }
	@$(ADB) $(ADB_TARGET) install -r "$(APK)"

run: install
	$(call log,$@)
	@$(ADB) $(ADB_TARGET) shell am start \
		-n "$(PACKAGE)/$(ACTIVITY)"

stop:
	$(call log,$@)
	@$(ADB) $(ADB_TARGET) shell am force-stop "$(PACKAGE)"

uninstall:
	$(call log,$@)
	-@$(ADB) $(ADB_TARGET) uninstall "$(PACKAGE)"

## ---------------------------------------------------------------------------
## Limpeza e diagnóstico
## ---------------------------------------------------------------------------

clean:
	$(call log,$@)
	@cd "$(ROOT)" && "$(GRADLEW)" $(MODULE):clean

logcat:
	$(call log,$@)
	@pid="$$($(ADB) $(ADB_TARGET) shell pidof -s \
		"$(PACKAGE)" | tr -d '\r')"; \
	test -n "$$pid" || \
		{ echo "Aplicativo não está executando"; exit 1; }; \
	$(ADB) $(ADB_TARGET) logcat --pid="$$pid"

devices:
	$(call log,$@)
	@$(ADB) devices -l
