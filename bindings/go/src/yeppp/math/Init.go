package math

//#include "yepLibrary.h"
//#cgo LDFLAGS: -lyeppp
import "C"
import "log"

func init() {
	status := C.yepLibrary_Init()
	if status != C.YepStatusOk {
		log.Fatal("Failed to initialize Yeppp! library")
	}
}
