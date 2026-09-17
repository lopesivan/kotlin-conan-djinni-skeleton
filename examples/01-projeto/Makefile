##############################################################################
# SHELL
##############################################################################
SHELL := /bin/bash

##############################################################################
# VARIÁVEIS GERAIS
##############################################################################
ROOT          := ../..
ANDROID_SDK   := /home/ivan/Android/Sdk
NDK_VERSION   := 29.0.14206865
ANDROID_NDK_HOME := $(ANDROID_SDK)/ndk/$(NDK_VERSION)
ADB           := $(ANDROID_SDK)/platform-tools/adb
GRADLEW       := $(ROOT)/gradlew
ABI           ?= arm64-v8a
CONAN_ARCH    := armv8
BUILD_TYPE    ?= Debug

#ADB_SELECTED_DEVICE := RX8N9045ELX
ADB_SELECTED_DEVICE := 7535c5b5

export ANDROID_NDK_HOME

##############################################################################
# INCLUDES
##############################################################################
include $(ROOT)/mk/tools.mk

##############################################################################
# MÓDULO
##############################################################################
MODULE_NAME := $(notdir $(CURDIR))
MODULE      := :examples:$(MODULE_NAME)
PACKAGE     := io.boden.examples.widgetsyoga
APK         := build/outputs/apk/debug/$(MODULE_NAME)-debug.apk
ACTIVITY    := io.boden.android.BodenActivity

LOCKFILE    := conan.lock

##############################################################################
# HELPERS
##############################################################################
log = @printf "\033[36m[make]\033[0m %s\n" "$(1)"

.DEFAULT_GOAL := help

##############################################################################
# INCLUDES ADICIONAIS
##############################################################################
include $(ROOT)/mk/onoff.mk
include $(ROOT)/mk/keycode.mk
include $(ROOT)/mk/asciinema.mk
include $(ROOT)/mk/scrcpy.mk
include $(ROOT)/mk/screen.mk
include $(ROOT)/mk/android_inter.mk
include $(ROOT)/mk/7535c5b5.mk

##############################################################################
# PHONY
##############################################################################
.PHONY: help init export-recipes deps deps-build build install run stop uninstall clean log-app \
        about version devices shell restart dry

##############################################################################
# AJUDA
##############################################################################
help:
	@printf "make init        verifica o ambiente\n"
	@printf "make deps-build  cria dependencias ausentes\n"
	@printf "make build       prepara Conan e compila\n"
	@printf "make install     compila e instala\n"
	@printf "make run         compila, instala e executa\n"

##############################################################################
# CONFIGURE — variáveis de ambiente
##############################################################################
configure: ## mostra as variáveis de ambiente usadas pelo Makefile
	$(call log,$@)
	@echo "=== Shell / Paths ==="
	@echo "SHELL              = $(SHELL)"
	@echo "ROOT               = $(ROOT)"
	@echo "ANDROID_SDK        = $(ANDROID_SDK)"
	@echo "NDK_VERSION        = $(NDK_VERSION)"
	@echo "ANDROID_NDK_HOME   = $(ANDROID_NDK_HOME)"
	@echo "ADB                = $(ADB)"
	@echo "GRADLEW            = $(GRADLEW)"
	@echo "LOCKFILE           = $(LOCKFILE)"

	@echo "=== Build ==="
	@echo "ABI                = $(ABI)"
	@echo "CONAN_ARCH         = $(CONAN_ARCH)"
	@echo "BUILD_TYPE         = $(BUILD_TYPE)"

	@echo "=== Dispositivo ==="
	@echo "ADB_SELECTED_DEVICE= $(ADB_SELECTED_DEVICE)"

	@echo "=== Módulo ==="
	@echo "MODULE_NAME        = $(MODULE_NAME)"
	@echo "MODULE             = $(MODULE)"
	@echo "PACKAGE            = $(PACKAGE)"
	@echo "APK                = $(APK)"
	@echo "ACTIVITY           = $(ACTIVITY)"

	@echo "=== Ambiente exportado ==="
	@env | grep -E '^(ANDROID_NDK_HOME|ANDROID_SDK_ROOT|ANDROID_HOME|JAVA_HOME|CONAN_)=' | sort || true

	@echo "=== ADB selecionado ==="
	@$(ADB) -s $(ADB_SELECTED_DEVICE) get-serialno 2>/dev/null \
		|| echo "(dispositivo $(ADB_SELECTED_DEVICE) nao conectado)"
##############################################################################
# AMBIENTE / BUILD / INSTALL / RUN
##############################################################################
init:
	$(call log,$@)
	@test -x "$(GRADLEW)" || { echo "gradlew nao encontrado"; exit 1; }
	@test -d "$(ANDROID_NDK_HOME)" || { echo "NDK nao encontrado"; exit 1; }
	@cd "$(ROOT)" && ./gradlew --version

export-recipes:
	$(call log,$@)
	@cd "$(ROOT)" && conan export recipes/yoga
	@cd "$(ROOT)" && conan export recipes/luapp
	@cd "$(ROOT)" && conan export .

deps: export-recipes
	$(call log,$@)
	@cd "$(ROOT)" && conan install examples/$(MODULE_NAME) --profile:build=profiles/linux-build \
		--profile:host=profiles/android-$(CONAN_ARCH) -s:h build_type=$(BUILD_TYPE) \
		-c:h "tools.android:ndk_path=$(ANDROID_NDK_HOME)" --lockfile=$(LOCKFILE) \
		--lockfile-partial --output-folder=.conan/android/$(CONAN_ARCH)/$(BUILD_TYPE) --build=never

deps-build: export-recipes
	$(call log,$@)
	@cd "$(ROOT)" && conan install examples/$(MODULE_NAME) --profile:build=profiles/linux-build \
		--profile:host=profiles/android-$(CONAN_ARCH) -s:h build_type=$(BUILD_TYPE) \
		-c:h "tools.android:ndk_path=$(ANDROID_NDK_HOME)" --lockfile=$(LOCKFILE) \
		--lockfile-partial --output-folder=.conan/android/$(CONAN_ARCH)/$(BUILD_TYPE) --build=missing

build: deps
	$(call log,$@)
	@cd "$(ROOT)" && ./gradlew $(MODULE):assembleDebug -PbodenAbis="$(ABI)"

install:
	$(call log,$@)
	$(ADB) install -r "$(APK)"

run:
	$(call log,$@)
	$(ADB) shell am start -n "$(PACKAGE)/$(ACTIVITY)"

stop:
	$(ADB) shell am force-stop "$(PACKAGE)"

restart: ## Forçar o restart da Activity (fecha e abre novamente em um único comando)
	$(call log,$@)
	$(START) -S -n $(PKG)/$(ACTIVITY)

uninstall:
	-$(ADB) uninstall "$(PACKAGE)"

clean:
	@cd "$(ROOT)" && ./gradlew $(MODULE):clean

##############################################################################
# LOGS
##############################################################################
log-app:
	@pid="$$($(ADB) shell pidof -s "$(PACKAGE)" | tr -d '\r')"; \
	 test -n "$$pid" || { echo "aplicativo nao esta executando"; exit 1; }; \
	 $(ADB) logcat --pid="$$pid"

##############################################################################
# DEVICE — informações e acesso básico
##############################################################################
about: ## mostra informações gerais do dispositivo
	$(call log,$@)
	@echo "=== Android ==="
	@$(ADB) shell getprop ro.build.version.release

	@echo "=== Device ==="
	@$(ADB) shell getprop ro.product.model

	@echo "=== Serial ==="
	@$(ADB) get-serialno

	@echo "=== Battery ==="
	@$(ADB) shell dumpsys battery | grep -E 'level|status|temperature'

	@echo "=== Uptime ==="
	@$(ADB) shell uptime

	@echo "=== IP ==="
	@$(ADB) shell ip addr show wlan0 | grep 'inet '

	@echo "=== CPU ==="
	@$(ADB) shell cat /proc/cpuinfo | grep -E 'Hardware|processor' | tail -2
	@$(ADB) shell cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq 2>/dev/null | awk '{printf "Freq: %d MHz\n", $$1/1000}'

	@echo "=== RAM ==="
	@$(ADB) shell cat /proc/meminfo | grep -E 'MemTotal|MemFree|MemAvailable'

	@echo "=== Screen ==="
	@$(ADB) shell wm size
	@$(ADB) shell wm density

	@echo "=== Build ==="
	@$(ADB) shell getprop ro.build.id
	@$(ADB) shell getprop ro.product.brand
	@$(ADB) shell getprop ro.product.device

	@echo "=== Processes ==="
	@$(ADB) shell ps | wc -l

	@echo "=== Storage ==="
	@$(ADB) shell '\
		echo "Internal : $$(df -h /data | tail -1 | awk '\''{print $$2 " total, " $$3 " used, " $$4 " free"}'\'')"; \
		echo "Linux    : $$(df -h /data/local/mnt | tail -1 | awk '\''{print $$2 " total, " $$3 " used, " $$4 " free"}'\'')"; \
		echo "SD Card  : $$(df -h /storage/6166-6564 | tail -1 | awk '\''{print $$2 " total, " $$3 " used, " $$4 " free"}'\'')"; \
		echo "Emulated : $$(df -h /storage/emulated/0 | tail -1 | awk '\''{print $$2 " total, " $$3 " used, " $$4 " free"}'\'')"; \
	'

version:
	$(call log,$@)
	@$(ADB_EXEC_OUT) cat /proc/version

devices: ## lista dispositivos conectados via ADB
	$(call log,$@)
	$(ADB) devices

shell: ## abre shell ADB
	$(call log,$@)
	$(ADB_SHELL)

##############################################################################
# APP — utilitários
##############################################################################
dry: ## Limpar todos os dados do app (fecha o app e limpa cache/storage
	$(call log,$@)
	$(PM) clear $(PKG)


test:
	unzip -l $(APK) | grep '\.so$$'
	readelf -d build/intermediates/cxx/Debug/*/obj/arm64-v8a/libwidgets_yoga_lua.so | grep NEEDED
