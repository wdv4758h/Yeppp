cmake_minimum_required(VERSION 2.8)

project(YepRT C)

set(YEPRT_ARMV7A_GCC_SOURCES
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_llsl.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_lmul.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_ul2d.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_uidiv.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_uidivmod.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_uldivmod.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/udivmoddi4.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/div_tables.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/memcpy.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/memcmp.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/memset.asm
)

set(YEPRT_ARMV5T_GCC_SOURCES
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dcmpeq.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dcmpge.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dcmpgt.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dcmple.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dcmplt.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dadd.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dsub.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_dmul.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_ddiv.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fcmpeq.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fcmpne.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fcmpge.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fcmpgt.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fcmple.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fcmplt.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fmul.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fadd.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_fsub.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_llsl.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_lmul.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_i2d.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_ui2f.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_ui2d.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_ul2d.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_ulcmp.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_uidiv.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_uidivmod.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/aeabi_uldivmod.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/udivmoddi4.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/eabi/div_tables.c
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/gnu_thumb1_case.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/memcpy.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/memcmp.asm
	${CMAKE_SOURCE_DIR}/sources/arm/gcc/memset.asm
)

set(YEPRT_MIPS_GCC_SOURCES
	${CMAKE_SOURCE_DIR}/sources/mips/gcc/ashldi3.asm
	${CMAKE_SOURCE_DIR}/sources/mips/gcc/memcmp.asm
	${CMAKE_SOURCE_DIR}/sources/mips/gcc/memcpy.asm
	${CMAKE_SOURCE_DIR}/sources/mips/gcc/memset.asm
	${CMAKE_SOURCE_DIR}/sources/mips/gcc/udivdi3.c
	${CMAKE_SOURCE_DIR}/sources/mips/gcc/floatdidf.c
)

set(YEPRT_X86_GCC_SOURCES
	${CMAKE_SOURCE_DIR}/sources/x86/gcc/udivdi3.asm
	${CMAKE_SOURCE_DIR}/sources/x86/memcmp.asm
	${CMAKE_SOURCE_DIR}/sources/x86/memcpy.asm
	${CMAKE_SOURCE_DIR}/sources/x86/memset.asm
)

set(YEPRT_X64_GCC_SOURCES
	${CMAKE_SOURCE_DIR}/sources/x86-64/gcc/memcmp.asm
	${CMAKE_SOURCE_DIR}/sources/x86-64/gcc/memcpy.asm
	${CMAKE_SOURCE_DIR}/sources/x86-64/gcc/memset.asm
)

set(YEPRT_X86_MSVC_SOURCES
	${CMAKE_SOURCE_DIR}/sources/x86/msvc/alldiv.asm
	${CMAKE_SOURCE_DIR}/sources/x86/msvc/aulldiv.asm
	${CMAKE_SOURCE_DIR}/sources/x86/msvc/allshl.asm
	${CMAKE_SOURCE_DIR}/sources/x86/msvc/allmul.asm
	${CMAKE_SOURCE_DIR}/sources/x86/msvc/fltused.asm
	${CMAKE_SOURCE_DIR}/sources/x86/memcmp.asm
	${CMAKE_SOURCE_DIR}/sources/x86/memcpy.asm
	${CMAKE_SOURCE_DIR}/sources/x86/memset.asm
)

set(YEPRT_X64_MSVC_SOURCES
	${CMAKE_SOURCE_DIR}/sources/x86-64/msvc/fltused.asm
	${CMAKE_SOURCE_DIR}/sources/x86-64/msvc/memcmp.asm
	${CMAKE_SOURCE_DIR}/sources/x86-64/msvc/memcpy.asm
	${CMAKE_SOURCE_DIR}/sources/x86-64/msvc/memset.asm
)

if(YEPPP_TARGET_NAME STREQUAL "linux-armel")
	enable_language(ASM-ATT)
	set(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM-ATT_FLAGS} -I${CMAKE_SOURCE_DIR}/sources/arm/gcc")
	set(CMAKE_ASM-ATT_COMPILE_OBJECT "<CMAKE_ASM-ATT_COMPILER> ${CMAKE_ASM-ATT_FLAGS} -o <OBJECT> <SOURCE>")
	set(YEPRT_SOURCES "${YEPRT_ARMV5T_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "linux-armhf")
	enable_language(ASM-ATT)
	set(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM-ATT_FLAGS} -I${CMAKE_SOURCE_DIR}/sources/arm/gcc")
	set(CMAKE_ASM-ATT_COMPILE_OBJECT "<CMAKE_ASM-ATT_COMPILER> ${CMAKE_ASM-ATT_FLAGS} -o <OBJECT> <SOURCE>")
	set(YEPRT_SOURCES "${YEPRT_ARMV7A_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "android-armeabi")
	enable_language(ASM-ATT)
	set(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM-ATT_FLAGS} -I${CMAKE_SOURCE_DIR}/sources/arm/gcc")
	set(CMAKE_ASM-ATT_COMPILE_OBJECT "<CMAKE_ASM-ATT_COMPILER> ${CMAKE_ASM-ATT_FLAGS} -o <OBJECT> <SOURCE>")
	set(YEPRT_SOURCES "${YEPRT_ARMV5T_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "android-armeabiv7a")
	enable_language(ASM-ATT)
	set(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM-ATT_FLAGS} -I${CMAKE_SOURCE_DIR}/sources/arm/gcc")
	set(CMAKE_ASM-ATT_COMPILE_OBJECT "<CMAKE_ASM-ATT_COMPILER> ${CMAKE_ASM-ATT_FLAGS} -o <OBJECT> <SOURCE>")
	set(YEPRT_SOURCES "${YEPRT_ARMV7A_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "android-mips")
	enable_language(ASM-ATT)
	set(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM-ATT_FLAGS} -I${CMAKE_SOURCE_DIR}/sources/mips/gcc")
	set(CMAKE_ASM-ATT_COMPILE_OBJECT "<CMAKE_ASM-ATT_COMPILER> ${CMAKE_ASM-ATT_FLAGS} -o <OBJECT> <SOURCE>")
	set(YEPRT_SOURCES "${YEPRT_MIPS_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "linux-x86")
	set(CMAKE_ASM_NASM_OBJECT_FORMAT elf32)
	enable_language(ASM_NASM)
	set(YEPRT_SOURCES "${YEPRT_X86_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "android-x86")
	set(CMAKE_ASM_NASM_OBJECT_FORMAT elf32)
	enable_language(ASM_NASM)
	set(YEPRT_SOURCES "${YEPRT_X86_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "linux-x86_64")
	set(CMAKE_ASM_NASM_OBJECT_FORMAT elf64)
	enable_language(ASM_NASM)
	set(YEPRT_SOURCES "${YEPRT_X64_GCC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "windows-x86")
	set(CMAKE_ASM_NASM_OBJECT_FORMAT win32)
	enable_language(ASM_NASM)
	set(YEPRT_SOURCES "${YEPRT_X86_MSVC_SOURCES}")
elseif(YEPPP_TARGET_NAME STREQUAL "windows-x86_64")
	set(CMAKE_ASM_NASM_OBJECT_FORMAT win64)
	enable_language(ASM_NASM)
	set(YEPRT_SOURCES "${YEPRT_X64_MSVC_SOURCES}")
else()
	message(FATAL_ERROR "Unsupported target ${YEPPP_TARGET_NAME}")
endif()

add_library(yeprt STATIC ${YEPRT_SOURCES})
