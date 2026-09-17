cmake_minimum_required(VERSION 3.23)

project(luapp VERSION 5.3.6 LANGUAGES CXX)

include(GNUInstallDirs)

set(LUAPP_ROOT
    "${CMAKE_CURRENT_SOURCE_DIR}/lua-5.3.6"
)

set(LUAPP_SOURCE_DIR
    "${LUAPP_ROOT}/src"
)

set(LUAPP_SOURCES
    "${LUAPP_SOURCE_DIR}/lapi.c"
    "${LUAPP_SOURCE_DIR}/lcode.c"
    "${LUAPP_SOURCE_DIR}/lctype.c"
    "${LUAPP_SOURCE_DIR}/ldebug.c"
    "${LUAPP_SOURCE_DIR}/ldo.c"
    "${LUAPP_SOURCE_DIR}/ldump.c"
    "${LUAPP_SOURCE_DIR}/lfunc.c"
    "${LUAPP_SOURCE_DIR}/lgc.c"
    "${LUAPP_SOURCE_DIR}/llex.c"
    "${LUAPP_SOURCE_DIR}/lmem.c"
    "${LUAPP_SOURCE_DIR}/lobject.c"
    "${LUAPP_SOURCE_DIR}/lopcodes.c"
    "${LUAPP_SOURCE_DIR}/lparser.c"
    "${LUAPP_SOURCE_DIR}/lstate.c"
    "${LUAPP_SOURCE_DIR}/lstring.c"
    "${LUAPP_SOURCE_DIR}/ltable.c"
    "${LUAPP_SOURCE_DIR}/ltm.c"
    "${LUAPP_SOURCE_DIR}/lundump.c"
    "${LUAPP_SOURCE_DIR}/lvm.c"
    "${LUAPP_SOURCE_DIR}/lzio.c"

    "${LUAPP_SOURCE_DIR}/lauxlib.c"
    "${LUAPP_SOURCE_DIR}/lbaselib.c"
    "${LUAPP_SOURCE_DIR}/lbitlib.c"
    "${LUAPP_SOURCE_DIR}/lcorolib.c"
    "${LUAPP_SOURCE_DIR}/ldblib.c"
    "${LUAPP_SOURCE_DIR}/liolib.c"
    "${LUAPP_SOURCE_DIR}/lmathlib.c"
    "${LUAPP_SOURCE_DIR}/loslib.c"
    "${LUAPP_SOURCE_DIR}/lstrlib.c"
    "${LUAPP_SOURCE_DIR}/ltablib.c"
    "${LUAPP_SOURCE_DIR}/lutf8lib.c"
    "${LUAPP_SOURCE_DIR}/loadlib.c"
    "${LUAPP_SOURCE_DIR}/linit.c"
)

# Embora os arquivos mantenham a extensão .c, esta variante do Lua
# deve ser integralmente compilada como C++.
set_source_files_properties(
    ${LUAPP_SOURCES}
    PROPERTIES
        LANGUAGE CXX
)

add_library(
    luapp
    SHARED
    ${LUAPP_SOURCES}
)

add_library(
    luapp::luapp
    ALIAS
    luapp
)

set_target_properties(
    luapp
    PROPERTIES
        OUTPUT_NAME "luapp5.3"
        POSITION_INDEPENDENT_CODE ON
        CXX_STANDARD 20
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
        CXX_VISIBILITY_PRESET default
        VISIBILITY_INLINES_HIDDEN OFF
)

target_include_directories(
    luapp
    PUBLIC
        $<BUILD_INTERFACE:${LUAPP_SOURCE_DIR}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/luapp>
)

target_compile_definitions(
    luapp
    PRIVATE
        LUA_USE_LINUX
)

target_compile_options(
    luapp
    PRIVATE
        -fexceptions
        -Wall
        -Wextra
)

if(ANDROID)
    target_link_libraries(
        luapp
        PRIVATE
            dl
            log
    )
else()
    target_link_libraries(
        luapp
        PRIVATE
            dl
    )
endif()

install(
    TARGETS luapp
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(
    FILES
        "${LUAPP_SOURCE_DIR}/lua.h"
        "${LUAPP_SOURCE_DIR}/luaconf.h"
        "${LUAPP_SOURCE_DIR}/lauxlib.h"
        "${LUAPP_SOURCE_DIR}/lualib.h"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/luapp"
)
