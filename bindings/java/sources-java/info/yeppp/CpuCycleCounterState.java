/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * The state of the processor cycle counter.
 * <p>
 * This class is intended to use only through {@link Library#acquireCycleCounter Library.acquireCycleCounter} and {@link Library#releaseCycleCounter Library.releaseCycleCounter} methods.
 *
 * @see	Library#acquireCycleCounter
 * @see	Library#releaseCycleCounter
 */
public final class CpuCycleCounterState {

	protected CpuCycleCounterState(long state) {
		this.state = state;
	}

	protected long state;

};
