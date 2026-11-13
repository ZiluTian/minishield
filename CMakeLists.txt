# Copyright (c) 2026 ZiluTian
#
# MiniShield code is licensed under MIT; see LICENSE.
# The MiniShield books (volume1, volume2, volume3, docs/, PLAN.md) are CC BY-NC 4.0.
cmake_minimum_required(VERSION 3.15)
project(MiniShield CXX)

# LLVM 23 headers require C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Find LLVM
set(LLVM_LINK_LLVM_DYLIB ON)
find_package(LLVM REQUIRED CONFIG)
message(STATUS "Found llvm ${LLVM_PACKAGE_VERSION} at ${LLVM_DIR}")
# NOTE: the installed (conda) LLVM does not provide LLVM.cmake / AddLLVM.cmake,
# so add_llvm_library is unavailable. Plain CMake + the imported target that
# LLVMConfig.cmake defines is the correct consumer pattern.
add_library(MiniShield MODULE
	lib/Plugin.cpp
	lib/FlatteningPass.cpp
	lib/StatsPass.cpp
	lib/CFGAnalyzer.cpp
	lib/FunctionEligibility.cpp
	lib/StateMachineBuilder.cpp
)

separate_arguments(MS_LLVM_DEFS NATIVE_COMMAND ${LLVM_DEFINITIONS})
target_compile_definitions(MiniShield PRIVATE ${MS_LLVM_DEFS})
target_include_directories(MiniShield PRIVATE
      ${LLVM_INCLUDE_DIRS}
      ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Imported target `LLVM` = libLLVM-23.so (dylib, created by LLVMConfig.cmake
# because LLVM_LINK_LLVM_DYLIB is yes for this build). Every LLVM symbol in
# the plugin resolves from the same library that opt itself loads.
target_link_libraries(MiniShield PRIVATE LLVM)

set_target_properties(MiniShield PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
