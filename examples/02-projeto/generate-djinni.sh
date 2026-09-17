#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$APP_DIR/../.." && pwd)"
IDL_FILE="$ROOT_DIR/projeto/djinni/native_api.djinni"
BUILD_DIR="$APP_DIR/build"
CONAN_DIR="$BUILD_DIR/conan/djinni-generator"
OUTPUT_DIR="$BUILD_DIR/generated/djinni"
SUPPORT_DIR="$BUILD_DIR/djinni-support-lib"
SUPPORT_REPOSITORY="https://github.com/cross-language-cpp/djinni-support-lib.git"
SUPPORT_COMMIT="c197712e6061e8d45d3a90c22e2f43ce8fe71d26"

command -v conan >/dev/null 2>&1 || {
    echo "ERRO: Conan 2 nao foi encontrado no PATH." >&2
    exit 1
}

command -v java >/dev/null 2>&1 || {
    echo "ERRO: Java nao foi encontrado no PATH." >&2
    exit 1
}

mkdir -p "$CONAN_DIR"

if [ ! -f "$CONAN_DIR/conanbuild.sh" ]; then
    conan install "$APP_DIR/conanfile.txt" \
        --output-folder="$CONAN_DIR" \
        --build=missing
fi

set +u
# shellcheck disable=SC1091
source "$CONAN_DIR/conanbuild.sh"
set -u

DJINNI_COMMAND="${DJINNI_COMMAND:-$(command -v djinni || true)}"
if [ -z "$DJINNI_COMMAND" ] || [ ! -x "$DJINNI_COMMAND" ]; then
    echo "ERRO: o executavel djinni nao foi localizado." >&2
    exit 1
fi

if [ ! -d "$SUPPORT_DIR/.git" ]; then
    rm -rf "$SUPPORT_DIR"
    git init -q "$SUPPORT_DIR"
    git -C "$SUPPORT_DIR" remote add origin "$SUPPORT_REPOSITORY"
    git -C "$SUPPORT_DIR" fetch -q --depth 1 origin "$SUPPORT_COMMIT"
    git -C "$SUPPORT_DIR" checkout -q --detach FETCH_HEAD
fi

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/cpp" "$OUTPUT_DIR/jni" "$OUTPUT_DIR/java"

"$DJINNI_COMMAND" \
    --idl "$IDL_FILE" \
    --cpp-out "$OUTPUT_DIR/cpp" \
    --cpp-namespace generated \
    --java-out "$OUTPUT_DIR/java" \
    --java-package br.eng.ivanlopes.projeto02.generated \
    --jni-out "$OUTPUT_DIR/jni" \
    --ident-jni-class NativeFooBar \
    --ident-jni-file NativeFooBar \
    --jni-generate-main true

test -f "$OUTPUT_DIR/cpp/native_api.hpp"
test -f "$OUTPUT_DIR/jni/NativeNativeApi.cpp"

if [ ! -f "$OUTPUT_DIR/java/NativeApi.java" ] &&
   [ ! -f "$OUTPUT_DIR/java/br/eng/ivanlopes/projeto02/generated/NativeApi.java" ]; then
    echo "ERRO: NativeApi.java nao foi gerado." >&2
    exit 1
fi

printf 'Djinni gerado em %s\n' "$OUTPUT_DIR"
