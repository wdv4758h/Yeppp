/*
 *     Daemon for access to energy counters without superuser privileges
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 * Author: rschoene
 */

#ifndef YEPPP_SERVER_H_
#define YEPPP_SERVER_H_

#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

struct counter_data {
	//  -2	Close server
	//   0	Release counter
	// 1-8	Acquire specific counter (see yepLibrary)
	int kind_counter;
	// The read value after releasing (or -1 if there was an error).
	double read_value;
	// The error code while acquiring or releasing.
	int error_code;
};

#ifdef __cplusplus
}
#endif

#endif /* YEPPP_SERVER_H_ */
