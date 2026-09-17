#!/usr/bin/env bash
set -euo pipefail

: "${ANDROID_NDK:=$HOME/Android/Sdk/ndk/29.0.14206865}"

API="${API:-35}"
ABI="${1:-arm64-v8a}"
V="${NGSPICE_VERSION:-47}"

case "$ABI" in
    arm64-v8a)
        TARGET="aarch64-linux-android"
        ;;

    armeabi-v7a)
        TARGET="armv7a-linux-androideabi"
        ;;

    x86_64)
        TARGET="x86_64-linux-android"
        ;;

    x86)
        TARGET="i686-linux-android"
        ;;

    *)
        echo "ABI não suportada: $ABI" >&2
        echo "Use uma destas opções:" >&2
        echo "  arm64-v8a" >&2
        echo "  armeabi-v7a" >&2
        echo "  x86_64" >&2
        echo "  x86" >&2
        exit 1
        ;;
esac

TOOLCHAIN="$ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64"

if [[ ! -d "$ANDROID_NDK" ]]; then
    echo "Android NDK não encontrado:" >&2
    echo "  $ANDROID_NDK" >&2
    exit 1
fi

if [[ ! -d "$TOOLCHAIN" ]]; then
    echo "Toolchain do Android NDK não encontrado:" >&2
    echo "  $TOOLCHAIN" >&2
    exit 1
fi

export CC="$TOOLCHAIN/bin/${TARGET}${API}-clang"
export CXX="$TOOLCHAIN/bin/${TARGET}${API}-clang++"
export AR="$TOOLCHAIN/bin/llvm-ar"
export AS="$CC"
export LD="$TOOLCHAIN/bin/ld.lld"
export NM="$TOOLCHAIN/bin/llvm-nm"
export RANLIB="$TOOLCHAIN/bin/llvm-ranlib"
export STRIP="$TOOLCHAIN/bin/llvm-strip"
export READELF="$TOOLCHAIN/bin/llvm-readelf"

for PROGRAM in "$CC" "$CXX" "$AR" "$RANLIB" "$STRIP" "$READELF"; do
    if [[ ! -x "$PROGRAM" ]]; then
        echo "Ferramenta não encontrada:" >&2
        echo "  $PROGRAM" >&2
        exit 1
    fi
done

export CFLAGS="-fPIC -O2"
export CXXFLAGS="-fPIC -O2"
export LDFLAGS="-fPIC"
export LIBS="-lm"

SOURCE_DIR="ngspice-${V}"
ARCHIVE="${SOURCE_DIR}.tar.gz"
BUILD_DIR="${SOURCE_DIR}/build-${ABI}"
OUTPUT="libngspice-${ABI}.so"

if [[ ! -f "$ARCHIVE" ]]; then
    echo "Código-fonte do ngspice não encontrado:" >&2
    echo "  $ARCHIVE" >&2
    exit 1
fi

echo "==> Preparando ngspice ${V}"
echo "    ABI: $ABI"
echo "    API: $API"
echo "    NDK: $ANDROID_NDK"
echo "    CC : $CC"

rm -rf "$SOURCE_DIR"
tar xzf "$ARCHIVE"

pushd "$SOURCE_DIR" >/dev/null

echo "==> Gerando arquivos do Autotools"

./autogen.sh

popd >/dev/null

mkdir -p "$BUILD_DIR"

pushd "$BUILD_DIR" >/dev/null

#
# Respostas antecipadas necessárias durante compilação cruzada.
#

export ac_cv_func_malloc_0_nonnull=yes
export ac_cv_func_realloc_0_nonnull=yes
export ac_cv_lib_pthread_pthread_mutex_lock=yes

export ac_cv_func_getpwent=no
export ac_cv_func_setpwent=no
export ac_cv_func_endpwent=no

export CPPFLAGS="-DHAVE_LIBPTHREAD=1"

echo "==> Configurando ngspice para $ABI"

../configure \
    --build="$(../config.guess)" \
    --host="$TARGET" \
    --with-ngshared \
    --disable-openmp \
    --disable-xspice \
    --disable-debug \
    --disable-static \
    --enable-shared \
    --without-x \
    --without-readline

echo "==> Compilando libngspice"

make -j"$(nproc)" V=1

popd >/dev/null

LIBRARY="$BUILD_DIR/src/.libs/libngspice.so"

if [[ ! -f "$LIBRARY" ]]; then
    echo "Erro: a biblioteca não foi gerada:" >&2
    echo "  $LIBRARY" >&2
    exit 1
fi

echo "==> Removendo símbolos desnecessários"

"$STRIP" --strip-unneeded "$LIBRARY"

cp -f "$LIBRARY" "$OUTPUT"

echo
echo "=============================================="
echo "Biblioteca gerada com sucesso"
echo "=============================================="
echo

ls -lh "$OUTPUT"

echo
echo "Arquitetura:"
"$READELF" -h "$OUTPUT" |
    grep -E 'Class:|Data:|Machine:'

echo
echo "Dependências:"
"$READELF" -d "$OUTPUT" |
    grep 'NEEDED' || true

echo
echo "Arquivo final:"
echo "  $(pwd)/$OUTPUT"
