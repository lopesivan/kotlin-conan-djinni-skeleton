SHELL := /bin/bash

ROOT        := ../..
ANDROID_SDK ?= /home/ivan/Android/Sdk
ADB         := $(ANDROID_SDK)/platform-tools/adb
GRADLEW     := $(ROOT)/gradlew
MODULE      := :examples:01-projeto
PACKAGE     := br.eng.ivanlopes.projeto01
ACTIVITY    := .MainActivity
APK         := build/outputs/apk/debug/01-projeto-debug.apk
ABI         ?= arm64-v8a
DEVICE      ?=

ADB_TARGET := $(if $(DEVICE),-s $(DEVICE),)

.DEFAULT_GOAL := help

.PHONY: help init djinni build install run stop uninstall clean logcat devices

help:
	@printf "make init       verifica Gradle, Conan, Java e ADB\n"
	@printf "make djinni     gera Java/JNI/C++ a partir do contrato\n"
	@printf "make build      gera Djinni e compila o APK debug\n"
	@printf "make install    compila e instala o APK\n"
	@printf "make run        instala e inicia o aplicativo\n"
	@printf "make logcat     mostra somente os logs do aplicativo\n"
	@printf "DEVICE=serial   seleciona um dispositivo ADB\n"

init:
	@test -x "$(GRADLEW)" || { echo "gradlew nao encontrado"; exit 1; }
	@command -v conan >/dev/null || { echo "Conan 2 nao encontrado"; exit 1; }
	@command -v java >/dev/null || { echo "Java nao encontrado"; exit 1; }
	@test -x "$(ADB)" || { echo "ADB nao encontrado em $(ADB)"; exit 1; }
	@cd "$(ROOT)" && ./gradlew --version
	@conan --version
	@java -version

djinni: init
	@cd "$(ROOT)" && ./gradlew $(MODULE):generateDjinni

build: init
	@cd "$(ROOT)" && ./gradlew $(MODULE):assembleDebug -PprojectAbis="$(ABI)"

install: build
	$(ADB) $(ADB_TARGET) install -r "$(APK)"

run: install
	$(ADB) $(ADB_TARGET) shell am start -n "$(PACKAGE)/$(ACTIVITY)"

stop:
	$(ADB) $(ADB_TARGET) shell am force-stop "$(PACKAGE)"

uninstall:
	-$(ADB) $(ADB_TARGET) uninstall "$(PACKAGE)"

clean:
	@cd "$(ROOT)" && ./gradlew $(MODULE):clean

logcat:
	@pid="$$($(ADB) $(ADB_TARGET) shell pidof -s "$(PACKAGE)" | tr -d '\r')"; \
	test -n "$$pid" || { echo "aplicativo nao esta executando"; exit 1; }; \
	$(ADB) $(ADB_TARGET) logcat --pid="$$pid"

devices:
	$(ADB) devices -l
