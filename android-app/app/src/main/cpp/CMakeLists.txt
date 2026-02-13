cmake_minimum_required(VERSION 3.22.1)

project("barh_native")

# Add the native library
add_library(
    barh_native
    SHARED
    barh_native.cpp
)

# Find required libraries
find_library(
    log-lib
    log
)

find_library(
    android-lib
    android
)

# Link libraries
target_link_libraries(
    barh_native
    ${log-lib}
    ${android-lib}
)
