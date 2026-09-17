SHELL := /bin/bash
ROOT  := ../..

## ---------------------------------------------------------------------------
## Caminhos do projeto
## ---------------------------------------------------------------------------

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
ADB   := $(ANDROID_SDK)/platform-tools/adb


CONAN ?= conan
JAVA  ?= java
GIT   ?= git

GRADLEW                   := $(ROOT)/gradlew
GRADLE_WRAPPER_DIR        := $(ROOT)/gradle/wrapper
GRADLE_WRAPPER_JAR        := $(GRADLE_WRAPPER_DIR)/gradle-wrapper.jar
GRADLE_WRAPPER_JAR_URL    := https://raw.githubusercontent.com/gradle/gradle/v$(GRADLE_VERSION)/gradle/wrapper/gradle-wrapper.jar
GRADLE_WRAPPER_JAR_SHA256 := 497c8c2a7e5031f6aa847f88104aa80a93532ec32ee17bdb8d1d2f67a194a9c7
LOCAL_PROPERTIES          := $(ROOT)/local.properties
DJINNI_SCRIPT             := generate-djinni.sh

##############################################################################
# MÓDULO
##############################################################################
MODULE_NAME := $(notdir $(CURDIR))
MODULE      := :examples:$(MODULE_NAME)
PACKAGE     := br.eng.ivanlopes.projeto01
ACTIVITY    := .MainActivity
APK         := build/outputs/apk/debug/$(MODULE_NAME)-debug.apk
ABI         ?= arm64-v8a

LOCKFILE    := conan.lock


ADB_SELECTED_DEVICE := 7535c5b5
ADB_SELECTED_DEVICE := RX8N9045ELX
DEVICE              ?= ADB_SELECTED_DEVICE

log = @printf "\033[36m[make]\033[0m %s\n" "$(1)"

.DEFAULT_GOAL := help

##############################################################################
# INCLUDES
##############################################################################
include $(ROOT)/mk/tools.mk
.PHONY: help wrapper init djinni build install run stop uninstall clean logcat devices

##############################################################################
# INCLUDES ADICIONAIS
##############################################################################
include $(ROOT)/mk/onoff.mk
include $(ROOT)/mk/keycode.mk
include $(ROOT)/mk/energy.mk
include $(ROOT)/mk/asciinema.mk
include $(ROOT)/mk/scrcpy.mk
include $(ROOT)/mk/screen.mk
include $(ROOT)/mk/android_inter.mk

ifdef ADB_SELECTED_DEVICE
include $(ROOT)/mk/$(ADB_SELECTED_DEVICE).mk
endif

## ---------------------------------------------------------------------------
## Ajuda
## ---------------------------------------------------------------------------

help:
	@printf "make wrapper    baixa e verifica o Gradle Wrapper JAR\n"
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

wrapper:
	$(call log,$@)
	@command -v curl >/dev/null 2>&1 || \
		{ echo "Erro: curl não encontrado"; exit 1; }
	@mkdir -p "$(GRADLE_WRAPPER_DIR)"
	@if [ -f "$(GRADLE_WRAPPER_JAR)" ] && \
		printf '%s  %s\n' \
			"$(GRADLE_WRAPPER_JAR_SHA256)" \
			"$(GRADLE_WRAPPER_JAR)" | sha256sum --check --status; then \
		echo "Gradle Wrapper JAR já existe"; \
	else \
		tmp="$(GRADLE_WRAPPER_JAR).tmp"; \
		trap 'rm -f "$$tmp"' EXIT; \
		curl --fail --location --silent --show-error \
			"$(GRADLE_WRAPPER_JAR_URL)" --output "$$tmp"; \
		printf '%s  %s\n' \
			"$(GRADLE_WRAPPER_JAR_SHA256)" "$$tmp" | \
			sha256sum --check --status || \
			{ echo "Erro: checksum inválido do Gradle Wrapper JAR"; exit 1; }; \
		mv "$$tmp" "$(GRADLE_WRAPPER_JAR)"; \
		trap - EXIT; \
		echo "Gradle Wrapper JAR baixado e verificado"; \
	fi

init: wrapper
	$(call log,$@)

	@test -d "$(ANDROID_SDK)" || \
		{ echo "Erro: SDK não encontrado em $(ANDROID_SDK)"; exit 1; }

	@test -d "$(ANDROID_NDK_HOME)" || \
		{ echo "Erro: NDK não encontrado em $(ANDROID_NDK_HOME)"; exit 1; }

	@test -n "$(ADB)" || \
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
	@"$(GRADLEW)" --version

## ---------------------------------------------------------------------------
## Geração de código
## ---------------------------------------------------------------------------

djinni:
	$(call log,$@)
	@"$(GRADLEW)" $(MODULE):generateDjinni

## ---------------------------------------------------------------------------
## Compilação, instalação e execução
## ---------------------------------------------------------------------------

build:
	$(call log,$@)
	@"$(GRADLEW)" $(MODULE):assembleDebug \
		-PprojectAbis="$(ABI)"

install:
	$(call log,$@)
	@test -f "$(APK)" || \
		{ echo "Erro: APK não encontrado em $(APK)"; exit 1; }
	@$(ADB) install -r "$(APK)"

run:
	$(call log,$@)
	@$(ADB) shell am start \
		-n "$(PACKAGE)/$(ACTIVITY)"

stop:
	$(call log,$@)
	@$(ADB) shell am force-stop "$(PACKAGE)"

restart: stop run ## encerra, reinstala e inicia a aplicação

uninstall:
	$(call log,$@)
	-@$(ADB) uninstall "$(PACKAGE)"

## ---------------------------------------------------------------------------
## Limpeza e diagnóstico
## ---------------------------------------------------------------------------

clean:
	$(call log,$@)
	"$(GRADLEW)" $(MODULE):clean

logcat:
	$(call log,$@)
	@pid="$$($(ADB) shell pidof -s \
		"$(PACKAGE)" | tr -d '\r')"; \
	test -n "$$pid" || \
		{ echo "Aplicativo não está executando"; exit 1; }; \
	$(ADB) logcat --pid="$$pid"

devices:
	$(call log,$@)
	@$(ADB) devices -l

shell: ## abre shell ADB
	$(call log,$@)
	$(ADB_SHELL)

##############################################################################
# APP — utilitários
##############################################################################
dry: ## Limpar todos os dados do app (fecha o app e limpa cache/storage)
	$(call log,$@)
	$(PM) clear $(PACKAGE)
