package library

//#include "yepLibrary.h"
//#cgo LDFLAGS: -lyeppp
import "C"

func GetTimerFrequency() uint64 {
	var frequency C.Yep64u = 0
	C.yepLibrary_GetTimerFrequency(&frequency)
	return uint64(frequency)
}

func GetTimerTicks() uint64 {
	var ticks C.Yep64u = 0
	C.yepLibrary_GetTimerTicks(&ticks)
	return uint64(ticks)
}
