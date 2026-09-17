#!/usr/bin/env bash
set -e

PWD_LOCAL=$PWD
V=5.3.6
R=${V%.?}

# --- NDK config ---
: "${ANDROID_NDK:=$HOME/Android/Sdk/ndk/29.0.14206865}"
API=24
ABI=${1:-arm64-v8a} # arm64-v8a | armeabi-v7a | x86_64 | x86

case $ABI in
    arm64-v8a) TARGET=aarch64-linux-android ;;
    armeabi-v7a) TARGET=armv7a-linux-androideabi ;;
    x86_64) TARGET=x86_64-linux-android ;;
    x86) TARGET=i686-linux-android ;;
    *)
        echo "ABI desconhecida: $ABI"
        exit 1
        ;;
esac

TOOLCHAIN=$ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64
CXX=$TOOLCHAIN/bin/${TARGET}${API}-clang++
AR=$TOOLCHAIN/bin/llvm-ar
RANLIB=$TOOLCHAIN/bin/llvm-ranlib
STRIP=$TOOLCHAIN/bin/llvm-strip

_d=lua-${V}
test -d $_d && rm -rf $_d
_f=lua-${V}.tar.gz
if ! test -e $_f; then
    wget https://www.lua.org/ftp/lua-${V}.tar.gz
fi
tar xvzf lua-${V}.tar.gz
pushd ${PWD_LOCAL}/lua-${V}
patch -p1 <../luapp.patch

sed -i \
    -e 's/"Lua for C++ "/"Lua "/' \
    -e 's/LUA_RELEASE "  Copyright (C) 1994/LUA_RELEASE " for C++  Copyright (C) 1994/' \
    src/lua.h

exit 0

# target "linux" dá LUA_USE_LINUX (dlopen etc, que o bionic tem),
# mas o MYLIBS embutido nele traz -lreadline, que não existe no NDK.
# Passar MYLIBS na linha de comando sobrescreve o valor do target.
make -j$(nproc) linux \
    CC="$CXX" \
    AR="$AR rcu" \
    RANLIB="$RANLIB" \
    MYCFLAGS="-x c++ -fPIC" \
    MYLIBS="-ldl"

_d=${HOME}/.luaenv/versions/${V}-android-${ABI}
test -d $_d && rm -rf $_d
mkdir -p \
    ${_d}/include \
    ${_d}/lib

cp src/*.h ${_d}/include/ 2>/dev/null || true

pushd src
$CXX -shared -Wl,-soname,libluapp${R}.so \
    -o libluapp${R}.so \
    $(ls *.o | grep -vE '^(lua|luac)\.o$') \
    -ldl
$STRIP --strip-unneeded libluapp${R}.so
cp libluapp${R}.so ${_d}/lib/
popd
popd
rm -rf ${PWD_LOCAL}/lua-${V}

echo "Gerado: ${_d}/lib/libluapp${R}.so (ABI $ABI)"
