set(CMAKE_SYSTEM_NAME "Linux")
set(CMAKE_SYSTEM_PROCESSOR "x86")

set(YEPPP_TARGET_NAME "linux-k1om")

include(utils)
if(NOT DEFINED YEPPP_ASM_COMPILER_PATH)
	file(TO_CMAKE_PATH $ENV{PATH} SEARCH_PATHS)
	set(BINUTILS_TARGET_REGEX "(k1om\\-mpss\\-linux)")
	foreach(SEARCH_DIR ${SEARCH_PATHS})
		search_cross_gas("${SEARCH_DIR}" "${BINUTILS_TARGET_REGEX}" YEPPP_ASM_COMPILER_PATH YEPPP_ASM_COMPILER_VERSION)
	endforeach(SEARCH_DIR)
	if(DEFINED YEPPP_ASM_COMPILER_PATH)
		message(STATUS "Found assembler at ${YEPPP_ASM_COMPILER_PATH}")
	else()
		message(FATAL_ERROR "No suitable assembler found")
	endif()
	set(YEPPP_ASM_COMPILER_PATH "${YEPPP_ASM_COMPILER_PATH}" CACHE FILEPATH "Path to assembler" FORCE)
endif()

include(CMakeForceCompiler)
CMAKE_FORCE_C_COMPILER("icc" Intel)
CMAKE_FORCE_CXX_COMPILER("icpc" Intel)
set(CMAKE_ASM-ATT_COMPILER  "${YEPPP_ASM_COMPILER_PATH}")

# Code-generation options
set(CMAKE_C_FLAGS "-mmic -nostdlib -fPIC -fno-asynchronous-unwind-tables -Wa,--noexecstack")
# Optimization options
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -ffunction-sections -fdata-sections -O3 -fomit-frame-pointer" CACHE STRING "")
# C++-specific options
set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -fno-rtti -fno-exceptions" CACHE STRING "")

# Target-specific options
set(CMAKE_ASM-ATT_FLAGS "-march=k1om")
# Code-generation options
set(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM-ATT_FLAGS} --noexecstack" CACHE STRING "")

# Linker options
set(CMAKE_SHARED_LINKER_FLAGS "-mmic -fPIC -nostdlib -Wl,-z,noexecstack -Wl,--no-undefined -Wl,--gc-sections" CACHE STRING "")
