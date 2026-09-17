cmake_minimum_required(VERSION 3.23)

project(project01_native LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

get_filename_component(PROJECT01_DIR "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)

set(DJINNI_GENERATED_DIR "${PROJECT01_DIR}/build/generated/djinni")
set(DJINNI_CPP_DIR "${DJINNI_GENERATED_DIR}/cpp")
set(DJINNI_JNI_DIR "${DJINNI_GENERATED_DIR}/jni")
set(DJINNI_SUPPORT_DIR "${PROJECT01_DIR}/build/djinni-support-lib")

file(GLOB DJINNI_JNI_SOURCES CONFIGURE_DEPENDS
    "${DJINNI_JNI_DIR}/*.cpp"
)

file(GLOB_RECURSE DJINNI_SUPPORT_SOURCES CONFIGURE_DEPENDS
    "${DJINNI_SUPPORT_DIR}/djinni/jni/*.cpp"
)

if(NOT DJINNI_JNI_SOURCES)
    message(FATAL_ERROR "Fontes JNI do Djinni ausentes. Execute a tarefa generateDjinni.")
endif()

if(NOT DJINNI_SUPPORT_SOURCES)
    message(FATAL_ERROR "djinni-support-lib ausente. Execute a tarefa generateDjinni.")
endif()

add_library(
    project01_native
    SHARED
    NativeApi.cpp
    ${DJINNI_JNI_SOURCES}
    ${DJINNI_SUPPORT_SOURCES}
)

target_include_directories(
    project01_native
    PRIVATE
    "${DJINNI_CPP_DIR}"
    "${DJINNI_JNI_DIR}"
    "${DJINNI_SUPPORT_DIR}"
)

target_link_libraries(
    project01_native
    PRIVATE
    android
    log
)
