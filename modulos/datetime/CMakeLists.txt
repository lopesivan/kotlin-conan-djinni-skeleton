cmake_minimum_required(VERSION 3.23)

project(boden_datetime VERSION 0.1.0 LANGUAGES CXX)

find_package(date REQUIRED CONFIG)

add_library(boden_datetime STATIC
    src/DateTime.cpp
)

add_library(boden::datetime ALIAS boden_datetime)

target_compile_features(boden_datetime PUBLIC cxx_std_20)

target_include_directories(boden_datetime
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(boden_datetime
    PUBLIC
        date::date
)

set_target_properties(boden_datetime PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)
