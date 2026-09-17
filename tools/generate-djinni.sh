#!/usr/bin/env sh
set -eu

if [ "$#" -ne 2 ]; then
    echo "uso: $0 CONTRATO.djinni DIRETORIO-SAIDA" >&2
    exit 2
fi

IDL_FILE=$1
OUTPUT_DIR=$2
DJINNI_COMMAND=${DJINNI_COMMAND:-djinni}

if ! command -v "$DJINNI_COMMAND" >/dev/null 2>&1; then
    echo "Djinni nao encontrado: $DJINNI_COMMAND" >&2
    echo "Defina DJINNI_COMMAND ou instale o gerador Djinni." >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR/cpp" "$OUTPUT_DIR/jni" "$OUTPUT_DIR/java"

exec "$DJINNI_COMMAND" \
    --idl "$IDL_FILE" \
    --cpp-out "$OUTPUT_DIR/cpp" \
    --cpp-namespace generated \
    --java-out "$OUTPUT_DIR/java" \
    --java-package br.eng.ivanlopes.nativeapi.generated \
    --jni-out "$OUTPUT_DIR/jni" \
    --ident-jni-class NativeFooBar \
    --ident-jni-file NativeFooBar \
    --jni-generate-main true

