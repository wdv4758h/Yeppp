set(CMAKE_SYSTEM_NAME "Windows")
set(CMAKE_SYSTEM_PROCESSOR "x86")

set(YEPPP_TARGET_NAME "windows-x86_64")

set(CMAKE_C_COMPILER "cl.exe")
set(CMAKE_CXX_COMPILER "cl.exe")
set(CMAKE_C_LINK_EXECUTABLE "link.exe")
set(CMAKE_CXX_LINK_EXECUTABLE "link.exe")
set(CMAKE_AR "lib.exe")
set(CMAKE_ASM_NASM_CREATE_STATIC_LIBRARY "<CMAKE_AR> /NOLOGO /NODEFAULTLIB /OUT:<TARGET> <LINK_FLAGS> <OBJECTS>")

# Use no runtime library
set(YEP_C_FLAGS_NO_RUNTIME "/Zl")
set(YEP_C_FLAGS_PIC_CODE "")

set(CMAKE_C_FLAGS "/nologo")
# Disable stack probes
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /GS-")
# Generate debug info
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /Z7")
# Optimized for speed
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /O2")

set(CMAKE_C_FLAGS_DEBUG "")
set(CMAKE_C_FLAGS_MINSIZEREL "")
set(CMAKE_C_FLAGS_RELEASE "")
set(CMAKE_C_FLAGS_RELWITHDEBINFO "")

# Disable RTTI
set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} /GR-")
# Disable exceptions
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHs-")

set(CMAKE_CXX_FLAGS_DEBUG "")
set(CMAKE_CXX_FLAGS_MINSIZEREL "")
set(CMAKE_CXX_FLAGS_RELEASE "")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "")

# Compile as C
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /TC" CACHE STRING "")
# Compile as C++
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /TP" CACHE STRING "")

set(CMAKE_ASM_NASM_OBJECT_FORMAT win64 CACHE STRING "")

# Linked options
#~ set(CMAKE_SHARED_LINKER_FLAGS "-m64 -fPIC -nostdlib -Wl,-z,noexecstack -Wl,--no-undefined -Wl,--gc-sections" CACHE STRING "")
