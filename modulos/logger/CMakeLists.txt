cmake_minimum_required(VERSION 3.23)

project(boden_logger VERSION 0.1.0 LANGUAGES CXX)

find_package(boden-datetime REQUIRED CONFIG)

add_library(boden_logger STATIC
    src/Logger.cpp
)

add_library(boden::logger ALIAS boden_logger)

target_compile_features(boden_logger PUBLIC cxx_std_20)

target_include_directories(boden_logger
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(boden_logger
    PUBLIC
        boden::datetime
)

set_target_properties(boden_logger PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)
