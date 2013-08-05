#!/bin/sh
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.

show_usage()
{
	echo "Usage: . set-vars.sh [param]"
	echo "   or source set-vars.sh [param]"
	echo "Possible options for [param]"
	echo "   x86    - set variables for x86 environment"
	echo "   x86_64 - set variables for x86-64 environment"
	echo "   k1om   - set variables for Xeon Phi environment"
	echo "   armel  - set variables for ARM Soft-Float EABI environment"
	echo "   armhf  - set variables for ARM Hard-Float EABI environment"
	echo "By default the variables are set according to OS architecture"
}

error_usage()
{
	echo "Error: invalid command-line argument(s)" >&2
	show_usage
}

error_arch()
{
	echo "Error: invalid architecture/ABI name $1" >&2
	show_usage
}

error_os()
{
	echo "Error: could not detect host OS: unknown kernel name $1" >&2
	echo "   Please refer to Yeppp! developers for a fix to this problem" >&2
}

error_os_arch()
{
	echo "Error: could not detect host architecture: unknown architecture name $2 for OS $1" >&2
	echo "   Please refer to Yeppp! developers for a fix to this problem" >&2
}

error_os_arch_abi()
{
	echo "Error: could not detect host ABI: unknown ABI name $3 for OS $1 on architecture $2" >&2
	echo "   Please refer to Yeppp! developers for a fix to this problem" >&2
}

error_shell()
{
	echo "Error: unknown Unix shell." >&2
	echo "   Please use bash, dash, zsh, or ksh" >&2
}

setup_universal()
{
	export YEPROOT="$1"

	if [ -z "${INCLUDE}" ]
	then
		export INCLUDE="${YEPROOT}/library/headers"
	else
		export INCLUDE="${YEPROOT}/library/headers:${INCLUDE}"
	fi

	if [ -z "${CPATH}" ]
	then
		export CPATH="${YEPROOT}/library/headers"
	else
		export CPATH="${YEPROOT}/library/headers:${CPATH}"
	fi

	if [ -z "${CLASSPATH}" ]
	then
		export CLASSPATH="${YEPROOT}/binaries/java-1.5/yeppp.jar"
	else
		export CLASSPATH="${YEPROOT}/binaries/java-1.5/yeppp.jar:${CLASSPATH}"
	fi
}

setup_x86()
{
	OS_KERNEL=$(uname -s)
	case "${OS_KERNEL}" in
		"Linux")
			export YEPPLATFORM="x86-linux-pic-i586"

			if [ -z "${LD_LIBRARY_PATH}" ]
			then
				export LD_LIBRARY_PATH="$1/binaries/linux/i586"
			else
				export LD_LIBRARY_PATH="$1/binaries/linux/i586:${LD_LIBRARY_PATH}"
			fi

			if [ -z "${LIBRARY_PATH}" ]
			then
				export LIBRARY_PATH="$1/binaries/linux/i586"
			else
				export LIBRARY_PATH="$1/binaries/linux/i586:${LIBRARY_PATH}"
			fi
		;;
		"Darwin")
			export YEPPLATFORM="x86-macosx-pic-default"

			if [ -z "$DYLD_LIBRARY_PATH" ]
			then
				export DYLD_LIBRARY_PATH="$1/binaries/macosx/x86"
			else
				export DYLD_LIBRARY_PATH="$1/binaries/macosx/x86:$DYLD_LIBRARY_PATH"
			fi

			if [ -z "${LIBRARY_PATH}" ]
			then
				export LIBRARY_PATH="$1/binaries/macosx/x86"
			else
				export LIBRARY_PATH="$1/binaries/macosx/x86:${LIBRARY_PATH}"
			fi
		;;
		*)
			error_os "${OS_KERNEL}"
			return 1
		;;
	esac
	setup_universal "$1"
	return 0
}

setup_x64()
{
	OS_KERNEL=$(uname -s)
	ARCHITECTURE=$(uname -m)
	case "${OS_KERNEL}" in
		"Linux")
			export YEPPLATFORM="x64-linux-sysv-default"

			if [ -z "${LD_LIBRARY_PATH}" ]
			then
				export LD_LIBRARY_PATH="$1/binaries/linux/x86_64"
			else
				export LD_LIBRARY_PATH="$1/binaries/linux/x86_64:${LD_LIBRARY_PATH}"
			fi

			if [ -z "${LIBRARY_PATH}" ]
			then
				export LIBRARY_PATH="$1/binaries/linux/x86_64"
			else
				export LIBRARY_PATH="$1/binaries/linux/x86_64:${LIBRARY_PATH}"
			fi
		;;
		"Darwin")
			export YEPPLATFORM="x64-macosx-sysv-default"

			if [ -z "$DYLD_LIBRARY_PATH" ]
			then
				export DYLD_LIBRARY_PATH="$1/binaries/macosx/x86_64"
			else
				export DYLD_LIBRARY_PATH="$1/binaries/macosx/x86_64:$DYLD_LIBRARY_PATH"
			fi

			if [ -z "${LIBRARY_PATH}" ]
			then
				export LIBRARY_PATH="$1/binaries/macosx/x86_64"
			else
				export LIBRARY_PATH="$1/binaries/macosx/x86_64:${LIBRARY_PATH}"
			fi
		;;
		*)
			error_os "${OS_KERNEL}"
			return 1
		;;
	esac
	setup_universal "$1"
	return 0
}

setup_k1om()
{
	# Compilation on Xeon Phi is not supported, so only need to setup LD_LIBRARY_PATH
	OS_KERNEL=$(uname -s)
	case "${OS_KERNEL}" in
		"Linux")
			export YEPPLATFORM="x64-linux-k1om-default"

			if [ -z "${LD_LIBRARY_PATH}" ]
			then
				export LD_LIBRARY_PATH="$1/binaries/linux/x86_64"
			else
				export LD_LIBRARY_PATH="$1/binaries/linux/x86_64:${LD_LIBRARY_PATH}"
			fi
		;;
		*)
			error_os
			return 1
		;;
	esac
	return 0
}

setup_armel()
{
	OS_KERNEL=$(uname -s)
	ARCHITECTURE=$(uname -m)
	case "${OS_KERNEL}" in
		"Linux")
			export YEPPLATFORM="arm-linux-softeabi-v5t"

			if [ -z "${LD_LIBRARY_PATH}" ]
			then
				export LD_LIBRARY_PATH="$1/binaries/linux/armel"
			else
				export LD_LIBRARY_PATH="$1/binaries/linux/armel:${LD_LIBRARY_PATH}"
			fi

			if [ -z "${LIBRARY_PATH}" ]
			then
				export LIBRARY_PATH="$1/binaries/linux/armel"
			else
				export LIBRARY_PATH="$1/binaries/linux/armel:${LIBRARY_PATH}"
			fi
		;;
		*)
			error_os "${OS_KERNEL}"
			return 1
		;;
	esac
	setup_universal "$1"
	return 0
}

setup_armhf()
{
	OS_KERNEL=$(uname -s)
	ARCHITECTURE=$(uname -m)
	case "${OS_KERNEL}" in
		"Linux")
			export YEPPLATFORM="arm-linux-hardeabi-v7a"

			if [ -z "${LD_LIBRARY_PATH}" ]
			then
				export LD_LIBRARY_PATH="$1/binaries/linux/armhf"
			else
				export LD_LIBRARY_PATH="$1/binaries/linux/armhf:${LD_LIBRARY_PATH}"
			fi

			if [ -z "${LIBRARY_PATH}" ]
			then
				export LIBRARY_PATH="$1/binaries/linux/armhf"
			else
				export LIBRARY_PATH="$1/binaries/linux/armhf:${LIBRARY_PATH}"
			fi
		;;
		*)
			error_os "${OS_KERNEL}"
			return 1
		;;
	esac
	setup_universal "$1"
	return 0
}

setup_guess()
{
	OS_KERNEL=$(uname -s)
	ARCHITECTURE=$(uname -m)
	if [ "${OS_KERNEL}"=="Linux" ]
	then
		case "${ARCHITECTURE}" in
			"i386"|"i486"|"i586"|"i686")
				setup_x86 "$1"
				return $?
			;;
			"x86_64")
				setup_x64 "$1"
				return $?
			;;
			"k1om")
				setup_k1om "$1"
				return $?
			;;
			"armv5tel"|"armv6l")
				dpkg --version >/dev/null 2>&1
				if [ "$?" -eq 0 ]
				then
					ABI=$(dpkg --print-architecture)
					if [ "${ABI}" == "armhf" ]
					then
						setup_armhf "$1"
						return $?
					elif [ "${ABI}" == "armel" ]
					then
						setup_armel "$1"
						return $?
					else
						error_os_arch_abi "${OS_KERNEL}" "${ARCHITECTURE}" "${ABI}"
					fi
				else
					echo "Warning: could reliably detect ABI. Assume soft-float ARM EABI" >&2
					setup_armel "$1"
					return $?
				fi
			;;
			"armv7l")
				dpkg --version >/dev/null 2>&1
				if [ "$?" -eq 0 ]
				then
					ABI=$(dpkg --print-architecture)
					if [ "${ABI}"=="armhf" ]
					then
						setup_armhf "$1"
						return $?
					elif [ "${ABI}"=="armel" ]
					then
						setup_armel "$1"
						return $?
					else
						error_os_arch_abi "${OS_KERNEL}" "${ARCHITECTURE}" "${ABI}"
					fi
				else
					echo "Warning: could reliably detect ABI. Assume hard-float ARM EABI" >&2
					setup_armhf "$1"
					return $?
				fi
			;;
			*)
				error_os_arch "${OS_KERNEL}" "${ARCHITECTURE}"
				return 1
			;;
		esac
	elif [ "${OS_KERNEL}"=="Darwin" ]
	then
		case "${ARCHITECTURE}" in
			"x86")
				setup_x86 "$1"
				return $?
			;;
			"x86_64")
				setup_x64 "$1"
				return $?
			;;
			*)
				error_os_arch "${OS_KERNEL}" "${ARCHITECTURE}"
				return 1
			;;
		esac
	else
		error_os "${OS_KERNEL}"
	fi
	setup_universal "$1"
	return 0
}

if [ -n "${BASH_SOURCE}" ]
then
	YEPROOT=$( cd $(dirname "${BASH_SOURCE}") ; pwd )
elif [ -n "${ZSH_VERSION}" ]
then
	YEPROOT=$( cd $(dirname "$0") ; pwd )
elif [ -n "${KSH_VERSION}" ]
then
	YEPROOT=$( cd $(dirname ${.sh.file}) ; pwd )
elif [ "$0"=="dash" ]
then
	echo "Warning: dash is only partially supported: architecture is always auto-detected" >&2
	YEP_SCRIPT_FD=`ls /proc/$$/fd/ | sort -nr | head -n 1`
	YEPROOT=$(dirname $(readlink "/proc/$$/fd/${YEP_SCRIPT_FD}"))
	unset YEP_SCRIPT_FD
	setup_guess "${YEPROOT}"
	return $?
else
	error_shell
	return 1
fi

if [ "$#" -eq 0 ]
then
	setup_guess "${YEPROOT}"
	return "$?"
elif [ "$#" -ne 1 ]
then
	error_usage
	return 1
fi

case "$1" in
	"x86")
		setup_x86 "${YEPROOT}"
		return "$?"
	;;
	"x86_64")
		setup_x64 "${YEPROOT}"
		return "$?"
	;;
	"k1om")
		setup_k1om "${YEPROOT}"
		return "$?"
	;;
	*)
		error_arch "$1"
		return 1
	;;
esac
