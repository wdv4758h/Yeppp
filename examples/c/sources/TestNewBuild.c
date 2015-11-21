#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#include <yepLibrary.h>
#include <yepCore.h>
#include <yepRandom.h>

/* Size of the array of elements to compute the polynomial on */
#define ARRAY_SIZE (1024*1024*8)


/* C implementation with hard-coded coefficients. The compilers should be good at optimizing it. */
void multiply_naive(const Yep64f *YEP_RESTRICT xArray, Yep64f *YEP_RESTRICT yArray, YepSize length) {
    for (YepSize i = 0; i < length; i++) {
        yArray[i] = xArray[i] * yArray[i];
    }
}


int main(int argc, char **argv) {
	enum YepStatus status;
	Yep64u startTimeNaive, startTimeYeppp, endTimeNaive, endTimeYeppp, frequency;
	Yep64f secsNaive, secsYeppp, flopsNaive, flopsYeppp;
	struct YepRandom_WELL1024a rng;

	/* Allocate arrays of inputs and outputs */
	Yep64f *x = (Yep64f*)calloc(ARRAY_SIZE, sizeof(Yep64f));
	Yep64f *pYeppp = (Yep64f*)calloc(ARRAY_SIZE, sizeof(Yep64f));
	Yep64f *pNaive = (Yep64f*)calloc(ARRAY_SIZE, sizeof(Yep64f));
	assert(x != NULL);
	assert(pYeppp != NULL);
	assert(pNaive != NULL);

	/* Initialize the Yeppp! library */
	status = yepLibrary_Init();
	assert(status == YepStatusOk);

	/* Initialize the random number generator */
	status = yepRandom_WELL1024a_Init(&rng);
	assert(status == YepStatusOk);

	/* Populate the array of inputs with random data */
	status = yepRandom_WELL1024a_GenerateUniform_S64fS64f_V64f_Acc64(&rng, 0.0, 100.0, x, ARRAY_SIZE);
	assert(status == YepStatusOk);

	/* Zero-initialize the output arrays */
	memset(pYeppp, 0, ARRAY_SIZE * sizeof(Yep64f));
	memset(pNaive, 0, ARRAY_SIZE * sizeof(Yep64f));

	/* Retrieve the number of timer ticks per second */
	status = yepLibrary_GetTimerFrequency(&frequency);
	assert(status == YepStatusOk);

	/* Retrieve the number of timer ticks before calling the C version of polynomial evaluation */
	status = yepLibrary_GetTimerTicks(&startTimeNaive);
	assert(status == YepStatusOk);

    multiply_naive(x, pNaive, ARRAY_SIZE);

	/* Retrieve the number of timer ticks after calling the C version of polynomial evaluation */
	status = yepLibrary_GetTimerTicks(&endTimeNaive);
	assert(status == YepStatusOk);

	/* Retrieve the number of timer ticks before calling Yeppp! polynomial evaluation */
	status = yepLibrary_GetTimerTicks(&startTimeYeppp);
	assert(status == YepStatusOk);

	/* Evaluate polynomial using Yeppp! */
	status = yepCore_Multiply_V64fV64f_V64f(x, pYeppp, pYeppp, ARRAY_SIZE);
	assert(status == YepStatusOk);

	/* Retrieve the number of timer ticks after calling Yeppp! polynomial evaluation */
	status = yepLibrary_GetTimerTicks(&endTimeYeppp);
	assert(status == YepStatusOk);

	/* Compute time in seconds and performance in FLOPS */
	secsNaive = ((Yep64f)(endTimeNaive - startTimeNaive)) / ((Yep64f)(frequency));
	secsYeppp = ((Yep64f)(endTimeYeppp - startTimeYeppp)) / ((Yep64f)(frequency));
	flopsNaive = (Yep64f)(ARRAY_SIZE) / secsNaive;
	flopsYeppp = (Yep64f)(ARRAY_SIZE) / secsYeppp;

	/* Report the timing and performance results */
	printf("Naive implementation:\n");
	printf("\tTime = %lf secs\n", secsNaive);
	printf("\tPerformance = %lf GFLOPS\n", flopsNaive * 1.0e-9);
	printf("Yeppp! implementation:\n");
	printf("\tTime = %lf secs\n", secsYeppp);
	printf("\tPerformance = %lf GFLOPS\n", flopsYeppp * 1.0e-9);


	/* Deinitialize the Yeppp! library */
	status = yepLibrary_Release();
	assert(status == YepStatusOk);

	/* Release the memory allocated for arrays */
	free(pYeppp);
	free(pNaive);
	free(x);

	return 0;
}
