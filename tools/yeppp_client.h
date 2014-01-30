/*
 *     Client to access to energy counters without superuser privileges
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 * Author: rschoene
 */

#ifndef YEPPP_CLIENT_H_
#define YEPPP_CLIENT_H_

#include <yeppp_server.h>

#define YEPPP_IP "127.0.0.1"
#define YEPPP_PORT 17037

#define ERROR_CODE_CLOSING_SOCKET	101
#define ERROR_CODE_INIT_SOCKET		102
#define ERROR_CODE_CONNCECTION		103
#define ERROR_CODE_SEND_GENERAL		104
#define ERROR_CODE_SEND_BYTES		105
#define ERROR_CODE_RECV_GENERAL		106
#define ERROR_CODE_RECV_BYTES		107
#define ERROR_CODE_RECV_SHUTDOWN	108

/** Copied from <yepLibrary.h>
 * @ingroup	yepLibrary_EnergyCounter
 * @brief	Energy counter type.
 * @see	yepLibrary_GetEnergyCounterAcquire
 */
enum YepEnergyCounterType {
	/** @brief	Intel RAPL per-package energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the energy (in Joules) consumed by all chips in the CPU package. */
	YepEnergyCounterTypeRaplPackageEnergy = 1,
	/** @brief	Intel RAPL power plane 0 energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the energy (in Joules) consumed by power plane 0 (includes CPU cores and caches). */
	YepEnergyCounterTypeRaplPowerPlane0Energy = 2,
	/** @brief	Intel RAPL power plane 1 energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the energy (in Joules) consumed by power plane 1 (includes GPU cores). */
	YepEnergyCounterTypeRaplPowerPlane1Energy = 3,
	/** @brief	Intel RAPL DRAM energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge E processors, and estimates the energy (in Joules) consumed by DRAM modules.
	 *          	Motherboard support is required to use this counter. */
	YepEnergyCounterTypeRaplDRAMEnergy = 4,
	/** @brief	Intel RAPL per-package power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the average power (in Watts) consumed by all chips in the CPU package.
	 *          	This counter is implemented as a combination of RAPL per-package energy counter and system timer. */
	YepEnergyCounterTypeRaplPackagePower = 5,
	/** @brief	Intel RAPL power plane 0 power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the average power (in Watts) consumed by power plane 0 (includes CPU cores and caches).
	 *          	This counter is implemented as a combination of RAPL power plane 0 energy counter and system timer. */
	YepEnergyCounterTypeRaplPowerPlane0Power = 6,
	/** @brief	Intel RAPL power plane 1 power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the average power (in Watts) consumed by power plane 1 (includes GPU cores).
	 *          	This counter is implemented as a combination of RAPL power plane 1 energy counter and system timer. */
	YepEnergyCounterTypeRaplPowerPlane1Power = 7,
	/** @brief	Intel RAPL DRAM power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge E processors, and estimates the average power (in Watts) consumed by DRAM modules.
	 *          	This counter is implemented as a combination of RAPL DRAM energy counter and system timer.
	 *          	Motherboard support is required to use this counter. */
	YepEnergyCounterTypeRaplDRAMPower = 8
};


int sendAndReceiveRequest(counter_data* request);

#endif /* YEPPP_CLIENT_H_ */
