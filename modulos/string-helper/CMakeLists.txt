cmake_minimum_required(VERSION 3.23)

project(boden_string VERSION 0.1.0 LANGUAGES CXX)

add_library(boden_string STATIC
    src/StringHelper.cpp
)

add_library(boden::string ALIAS boden_string)

target_compile_features(boden_string PUBLIC cxx_std_20)

target_include_directories(boden_string
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

set_target_properties(boden_string PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)
