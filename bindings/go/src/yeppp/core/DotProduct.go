package core

//#include "yepCore.h"
//#cgo LDFLAGS: -lyeppp
import "C"

func DotProduct_V64fV64f_S64f(x []float64, y []float64) float64 {
	var z float64 = 0.0
	if (len(x) == len(y)) {
		C.yepCore_DotProduct_V64fV64f_S64f((*C.Yep64f)(&x[0]), (*C.Yep64f)(&y[0]), (*C.Yep64f)(&z), C.YepSize(len(x)))
	}
	return z
}
