package math

//#include "yepMath.h"
//#cgo LDFLAGS: -lyeppp
import "C"

func Log_V64f_V64f(x []float64, y []float64) {
	if (len(x) == len(y)) {
		C.yepMath_Log_V64f_V64f((*C.Yep64f)(&x[0]), (*C.Yep64f)(&y[0]), C.YepSize(len(x)))
	}
}
