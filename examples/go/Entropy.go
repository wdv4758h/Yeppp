package main

import (
	"fmt"
	"math"
	"math/rand"

	yepLibrary "yeppp/library"
	yepCore "yeppp/core"
	yepMath "yeppp/math"
)

const arraySize = 1024*1024*16

func main() {
	/* Allocate an array of probabilities */
	p := make([]float64, arraySize)

	/* Populate the array of probabilities with random probabilities */
	for i := range p {
		/* 0 < p[i] <= 1.0 */
		p[i] = rand.Float64()
	}

	/* Retrieve the number of timer ticks per second */
	frequency := yepLibrary.GetTimerFrequency()

	/* Retrieve the number of timer ticks before calling naive entropy computation */
	startTimeNaive := yepLibrary.GetTimerTicks()

	/* Compute entropy using naive implementation */
	entropyNaive := computeEntropyNaive(p)

	/* Retrieve the number of timer ticks after calling naive entropy computation */
	endTimeNaive := yepLibrary.GetTimerTicks()

	/* Retrieve the number of timer ticks before calling Yeppp!-based entropy computation */
	startTimeYeppp := yepLibrary.GetTimerTicks()

	/* Compute entropy using Yeppp!-based implementation */
	entropyYeppp := computeEntropyYeppp(p)

	/* Retrieve the number of timer ticks after calling Yeppp!-based entropy computation */
	endTimeYeppp := yepLibrary.GetTimerTicks()

	/* Report the results */
	fmt.Println("Naive implementation:")
	fmt.Printf("\tEntropy = %f\n", entropyNaive)
	fmt.Printf("\tTime = %f\n", float64(endTimeNaive - startTimeNaive) / float64(frequency))
	fmt.Println("Yeppp! implementation:")
	fmt.Printf("\tEntropy = %f\n", entropyYeppp)
	fmt.Printf("\tTime = %f\n", float64(endTimeYeppp - startTimeYeppp) / float64(frequency))
}

/* The naive implementation of entropy computation using log function for LibM */
func computeEntropyNaive(probabilities []float64) float64 {
	var entropy float64 = 0.0
	for _, p := range probabilities {
		entropy -= p * math.Log(p)
	}
	return entropy
}

/* The implementation of entropy computation using vector log and dot-product functions from Yeppp! library */
/* To avoid allocating a large array for logarithms (and also to benefit from cache locality) the logarithms are computed on small blocks of the input array */
/* The size of the block used to compute the logarithm */
const blockSize = 1024
func computeEntropyYeppp(p []float64) float64 {
	var entropy float64 = 0.0
	/* The small array for computed logarithms of the part of the input array */
	var logP [blockSize]float64

	for index := 0; index < len(p); index += blockSize {
		/* Process min(BLOCK_SIZE, number of remaining elements) elements of the input array */
		blockLength := len(p) - index
		if blockLength > blockSize {
			blockLength = blockSize
		}

		/* Compute logarithms of probabilities in the current block of the input array */
		yepMath.Log_V64f_V64f(p[index:index+blockLength], logP[:])

		/* Compute the dot product of probabilities and log-probabilities of the current block */
		/* This will give minus entropy of the current block */
		dotProduct := yepCore.DotProduct_V64fV64f_S64f(p[index:index+blockLength], logP[:])

		/* Compute entropy of the current block and subtract it from the current entropy value */
		entropy -= dotProduct
	}
	return entropy
}


