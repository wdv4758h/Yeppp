package main

import (
	"fmt"
	"math"
	"math/rand"

	yepLibrary "yeppp/library"
	yepMath "yeppp/math"
)

/* Size of the array of elements to compute the polynomial on */
const arraySize = 1024*1024*8

/* Polynomial Coefficients 101 */
const c0   float64 = 1.53270461724076346
const c1   float64 = 1.45339856462100293
const c2   float64 = 1.21078763026010761
const c3   float64 = 1.46952786401453397
const c4   float64 = 1.34249847863665017
const c5   float64 = 0.75093174077762164
const c6   float64 = 1.90239336671587562
const c7   float64 = 1.62162053962810579
const c8   float64 = 0.53312230473555923
const c9   float64 = 1.76588453111778762
const c10  float64 = 1.31215699612484679
const c11  float64 = 1.49636144227257237
const c12  float64 = 1.52170011054112963
const c13  float64 = 0.83637497322280110
const c14  float64 = 1.12764540941736043
const c15  float64 = 0.65513628703807597
const c16  float64 = 1.15879020877781906
const c17  float64 = 1.98262901973751791
const c18  float64 = 1.09134643523639479
const c19  float64 = 1.92898634047221235
const c20  float64 = 1.01233347751449659
const c21  float64 = 1.89462732589369078
const c22  float64 = 1.28216239080886344
const c23  float64 = 1.78448898277094016
const c24  float64 = 1.22382217182612910
const c25  float64 = 1.23434674193555734
const c26  float64 = 1.13914782832335501
const c27  float64 = 0.73506235075797319
const c28  float64 = 0.55461432517332724
const c29  float64 = 1.51704871121967963
const c30  float64 = 1.22430234239661516
const c31  float64 = 1.55001237689160722
const c32  float64 = 0.84197209952298114
const c33  float64 = 1.59396169927319749
const c34  float64 = 0.97067044414760438
const c35  float64 = 0.99001960195021281
const c36  float64 = 1.17887814292622884
const c37  float64 = 0.58955609453835851
const c38  float64 = 0.58145654861350322
const c39  float64 = 1.32447212043555583
const c40  float64 = 1.24673632882394241
const c41  float64 = 1.24571828921765111
const c42  float64 = 1.21901343493503215
const c43  float64 = 1.89453941213996638
const c44  float64 = 1.85561626872427416
const c45  float64 = 1.13302165522004133
const c46  float64 = 1.79145993815510725
const c47  float64 = 1.59227069037095317
const c48  float64 = 1.89104468672467114
const c49  float64 = 1.78733894997070918
const c50  float64 = 1.32648559107345081
const c51  float64 = 1.68531055586072865
const c52  float64 = 1.08980909640581993
const c53  float64 = 1.34308207822154847
const c54  float64 = 1.81689492849547059
const c55  float64 = 1.38582137073988747
const c56  float64 = 1.04974901183570510
const c57  float64 = 1.14348742300966456
const c58  float64 = 1.87597730040483323
const c59  float64 = 0.62131555899466420
const c60  float64 = 0.64710935668225787
const c61  float64 = 1.49846610600978751
const c62  float64 = 1.07834176789680957
const c63  float64 = 1.69130785175832059
const c64  float64 = 1.64547687732258793
const c65  float64 = 1.02441150427208083
const c66  float64 = 1.86129006037146541
const c67  float64 = 0.98309038830424073
const c68  float64 = 1.75444578237500969
const c69  float64 = 1.08698336765112349
const c70  float64 = 1.89455010772036759
const c71  float64 = 0.65812118412299539
const c72  float64 = 0.62102711487851459
const c73  float64 = 1.69991208083436747
const c74  float64 = 1.65467704495635767
const c75  float64 = 1.69599459626992174
const c76  float64 = 0.82365682103308750
const c77  float64 = 1.71353437063595036
const c78  float64 = 0.54992984722831769
const c79  float64 = 0.54717367088443119
const c80  float64 = 0.79915543248858154
const c81  float64 = 1.70160318364006257
const c82  float64 = 1.34441280175456970
const c83  float64 = 0.79789486341474966
const c84  float64 = 0.61517383020710754
const c85  float64 = 0.55177400048576055
const c86  float64 = 1.43229889543908696
const c87  float64 = 1.60658663666266949
const c88  float64 = 1.78861146369896090
const c89  float64 = 1.05843250742401821
const c90  float64 = 1.58481799048208832
const c91  float64 = 1.70954313374718085
const c92  float64 = 0.52590070195022226
const c93  float64 = 0.92705074709607885
const c94  float64 = 0.71442651832362455
const c95  float64 = 1.14752795948077643
const c96  float64 = 0.89860175106926404
const c97  float64 = 0.76771198245570573
const c98  float64 = 0.67059202034800746
const c99  float64 = 0.53785922275590729
const c100 float64 = 0.82098327929734880

/* The same coefficients as an array. This array is used for a Yeppp! function call. */
var coefs = [101]float64 {
	 c0,  c1,  c2,  c3,  c4,  c5,  c6,  c7,  c8,  c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19,
	c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31, c32, c33, c34, c35, c36, c37, c38, c39,
	c40, c41, c42, c43, c44, c45, c46, c47, c48, c49, c50, c51, c52, c53, c54, c55, c56, c57, c58, c59,
	c60, c61, c62, c63, c64, c65, c66, c67, c68, c69, c70, c71, c72, c73, c74, c75, c76, c77, c78, c79,
	c80, c81, c82, c83, c84, c85, c86, c87, c88, c89, c90, c91, c92, c93, c94, c95, c96, c97, c98, c99,
	c100 }

/* Go implementation with hard-coded coefficients. The compilers should be good at optimizing it. */
func evaluatePolynomialNaive(xArray []float64, yArray []float64) {
	for index := range xArray {
		x := xArray[index]
		y := c100
		y = c99 + x * y
		y = c98 + x * y
		y = c97 + x * y
		y = c96 + x * y
		y = c95 + x * y
		y = c94 + x * y
		y = c93 + x * y
		y = c92 + x * y
		y = c91 + x * y
		y = c90 + x * y
		y = c89 + x * y
		y = c88 + x * y
		y = c87 + x * y
		y = c86 + x * y
		y = c85 + x * y
		y = c84 + x * y
		y = c83 + x * y
		y = c82 + x * y
		y = c81 + x * y
		y = c80 + x * y
		y = c79 + x * y
		y = c78 + x * y
		y = c77 + x * y
		y = c76 + x * y
		y = c75 + x * y
		y = c74 + x * y
		y = c73 + x * y
		y = c72 + x * y
		y = c71 + x * y
		y = c70 + x * y
		y = c69 + x * y
		y = c68 + x * y
		y = c67 + x * y
		y = c66 + x * y
		y = c65 + x * y
		y = c64 + x * y
		y = c63 + x * y
		y = c62 + x * y
		y = c61 + x * y
		y = c60 + x * y
		y = c59 + x * y
		y = c58 + x * y
		y = c57 + x * y
		y = c56 + x * y
		y = c55 + x * y
		y = c54 + x * y
		y = c53 + x * y
		y = c52 + x * y
		y = c51 + x * y
		y = c50 + x * y
		y = c49 + x * y
		y = c48 + x * y
		y = c47 + x * y
		y = c46 + x * y
		y = c45 + x * y
		y = c44 + x * y
		y = c43 + x * y
		y = c42 + x * y
		y = c41 + x * y
		y = c40 + x * y
		y = c39 + x * y
		y = c38 + x * y
		y = c37 + x * y
		y = c36 + x * y
		y = c35 + x * y
		y = c34 + x * y
		y = c33 + x * y
		y = c32 + x * y
		y = c31 + x * y
		y = c30 + x * y
		y = c29 + x * y
		y = c28 + x * y
		y = c27 + x * y
		y = c26 + x * y
		y = c25 + x * y
		y = c24 + x * y
		y = c23 + x * y
		y = c22 + x * y
		y = c21 + x * y
		y = c20 + x * y
		y = c19 + x * y
		y = c18 + x * y
		y = c17 + x * y
		y = c16 + x * y
		y = c15 + x * y
		y = c14 + x * y
		y = c13 + x * y
		y = c12 + x * y
		y = c11 + x * y
		y = c10 + x * y
		y = c9 + x * y
		y = c8 + x * y
		y = c7 + x * y
		y = c6 + x * y
		y = c5 + x * y
		y = c4 + x * y
		y = c3 + x * y
		y = c2 + x * y
		y = c1 + x * y
		y = c0 + x * y
		yArray[index] = y
	}
}

/* This function computes the maximum relative error between two vectors. */
func computeMaxError(xArray []float64, yArray []float64) float64 {
	var maxError float64 = 0.0
	for index := range xArray {
		if xArray[index] == 0.0 {
			continue
		}
		maxError = math.Max(maxError, math.Abs(xArray[index] - yArray[index]) / math.Abs(xArray[index]))
	}
	return maxError
}

func main() {
	/* Allocate arrays of inputs and outputs */
	x := make([]float64, arraySize)
	pYeppp := make([]float64, arraySize)
	pNaive := make([]float64, arraySize)

	/* Populate the array of inputs with random data */
	for i := range x {
		x[i] = rand.Float64()
	}

	/* Retrieve the number of timer ticks per second */
	frequency := yepLibrary.GetTimerFrequency()

	/* Retrieve the number of timer ticks before calling the Go version of polynomial evaluation */
	startTimeNaive := yepLibrary.GetTimerTicks()

	/* Evaluate polynomial using Go implementation */
	evaluatePolynomialNaive(x, pNaive)

	/* Retrieve the number of timer ticks after calling the Go version of polynomial evaluation */
	endTimeNaive := yepLibrary.GetTimerTicks()

	/* Retrieve the number of timer ticks before calling Yeppp! polynomial evaluation */
	startTimeYeppp := yepLibrary.GetTimerTicks()

	/* Evaluate polynomial using Yeppp! */
	yepMath.EvaluatePolynomial_V64fV64f_V64f(coefs[:], x, pYeppp)

	/* Retrieve the number of timer ticks after calling Yeppp! polynomial evaluation */
	endTimeYeppp := yepLibrary.GetTimerTicks()

	/* Compute time in seconds and performance in FLOPS */
	secsNaive := float64(endTimeNaive - startTimeNaive) / float64(frequency)
	secsYeppp := float64(endTimeYeppp - startTimeYeppp) / float64(frequency)
	flopsNaive := float64(arraySize * (len(coefs) - 1) * 2) / secsNaive
	flopsYeppp := float64(arraySize * (len(coefs) - 1) * 2) / secsYeppp

	/* Report the timing and performance results */
	fmt.Println("Naive implementation:")
	fmt.Printf("\tTime = %f secs\n", secsNaive)
	fmt.Printf("\tPerformance = %f GFLOPS\n", flopsNaive * 1.0e-9)
	fmt.Println("Yeppp! implementation:")
	fmt.Printf("\tTime = %f secs\n", secsYeppp)
	fmt.Printf("\tPerformance = %f GFLOPS\n", flopsYeppp * 1.0e-9)

	/* Make sure the result is correct. */
	fmt.Printf("Max error: %7.3f%%\n", computeMaxError(pNaive, pYeppp) * 100.0)
}
