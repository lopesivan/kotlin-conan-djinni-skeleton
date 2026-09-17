cmake_minimum_required(VERSION 3.23)

project(boden_file_helper VERSION 0.1.0 LANGUAGES CXX)

add_library(boden_file_helper STATIC
    src/FileHelper.cpp
)

add_library(boden::file-helper ALIAS boden_file_helper)

target_compile_features(boden_file_helper PUBLIC cxx_std_20)

target_include_directories(boden_file_helper
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

set_target_properties(boden_file_helper PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)
