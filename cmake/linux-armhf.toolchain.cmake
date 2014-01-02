MESSAGE("Building for linux/armhf")

SET(CMAKE_SYSTEM_NAME "Linux")
set(CMAKE_SYSTEM_PROCESSOR "arm")

SET(YEPPP_TARGET_NAME "linux-armhf")

include(utils)
if(NOT DEFINED YEPPP_C_COMPILER_PATH)
	file(TO_CMAKE_PATH $ENV{PATH} SEARCH_PATHS)
	set(GCC_TARGET_REGEX "arm\\-linux\\-gnueabihf")
	set(BINUTILS_TARGET_REGEX "arm\\-linux\\-gnueabihf")
	set(GCC_NAME_REGEX "(\\[A-Za-z0-9_]+\\-)*gcc(\\-[0-9]+(\\.[0-9]+)*)?$")
	set(GXX_NAME_REGEX "(\\[A-Za-z0-9_]+\\-)*g\\+\\+(\\-[0-9]+(\\.[0-9]+)*)?$")
	foreach(SEARCH_DIR ${SEARCH_PATHS})
		search_cross_gcc("${SEARCH_DIR}" "gcc" "${GCC_NAME_REGEX}" "${GCC_TARGET_REGEX}" YEPPP_C_COMPILER_PATH YEPPP_C_COMPILER_VERSION)
		search_cross_gcc("${SEARCH_DIR}" "g++" "${GXX_NAME_REGEX}" "${GCC_TARGET_REGEX}" YEPPP_CXX_COMPILER_PATH YEPPP_CXX_COMPILER_VERSION)
		search_cross_gas("${SEARCH_DIR}" "${BINUTILS_TARGET_REGEX}" YEPPP_ASM_COMPILER_PATH YEPPP_ASM_COMPILER_VERSION)
	endforeach(SEARCH_DIR)
	if(DEFINED YEPPP_C_COMPILER_PATH)
		message(STATUS "Found C compiler at ${YEPPP_C_COMPILER_PATH}")
	else()
		message(FATAL_ERROR "No suitable C compiler found")
	endif()
	if(DEFINED YEPPP_CXX_COMPILER_PATH)
		message(STATUS "Found C++ compiler at ${YEPPP_CXX_COMPILER_PATH}")
	else()
		message(FATAL_ERROR "No suitable C++ compiler found")
	endif()
	if(DEFINED YEPPP_ASM_COMPILER_PATH)
		message(STATUS "Found assembler at ${YEPPP_ASM_COMPILER_PATH}")
	else()
		message(FATAL_ERROR "No suitable assembler found")
	endif()
	set(YEPPP_C_COMPILER_PATH "${YEPPP_C_COMPILER_PATH}" CACHE FILEPATH "Path to C compiler" FORCE)
	set(YEPPP_CXX_COMPILER_PATH "${YEPPP_CXX_COMPILER_PATH}" CACHE FILEPATH "Path to C++ compiler" FORCE)
	set(YEPPP_ASM_COMPILER_PATH "${YEPPP_ASM_COMPILER_PATH}" CACHE FILEPATH "Path to assembler" FORCE)
endif()

include(CMakeForceCompiler)
CMAKE_FORCE_C_COMPILER("${YEPPP_C_COMPILER_PATH}" GNU)
CMAKE_FORCE_CXX_COMPILER("${YEPPP_CXX_COMPILER_PATH}" GNU)
SET(CMAKE_ASM-ATT_COMPILER "${YEPPP_ASM_COMPILER_PATH}")

# Target-specific options
SET(CMAKE_C_FLAGS "-marm -march=armv7-a -mtune=cortex-a9 -mfloat-abi=hard -mfpu=vfpv3")
# Code-generation options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -nostdlib -fPIC -Wno-psabi -fno-unwind-tables -Wa,--noexecstack")
# Optimization options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -ffunction-sections -fdata-sections -O3 -fomit-frame-pointer" CACHE STRING "")
# C++-specific options
set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -fno-rtti -fno-exceptions" CACHE STRING "")

# Target-specific options
SET(CMAKE_ASM-ATT_FLAGS "-march=armv7-a")
# Code-generation options
SET(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM-ATT_FLAGS} -Wa,--noexecstack" CACHE STRING "")

# Linked options
set(CMAKE_SHARED_LINKER_FLAGS "-fPIC -nostdlib -Wl,-z,noexecstack -Wl,--no-undefined -Wl,--gc-sections" CACHE STRING "")
