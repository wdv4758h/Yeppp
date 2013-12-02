package math

//#include "yepMath.h"
//#cgo LDFLAGS: -lyeppp
import "C"

func EvaluatePolynomial_V64fV64f_V64f(coef []float64, x []float64, y []float64) {
	if (len(x) == len(y)) {
		C.yepMath_EvaluatePolynomial_V64fV64f_V64f((*C.Yep64f)(&coef[0]), (*C.Yep64f)(&x[0]), (*C.Yep64f)(&y[0]), C.YepSize(len(coef)), C.YepSize(len(x)))
	}
}
