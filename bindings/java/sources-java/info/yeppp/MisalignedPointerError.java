/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

package info.yeppp;

/**
 * @brief	Misaligned pointer error
 * @details	This exception is thrown when a pointer passed to @Yeppp function is not properly aligned.
 */
public class MisalignedPointerError extends Error {
	
	/**
	 * @brief	Constructs a misaligned pointer error with the specified description.
	 */
	public MisalignedPointerError(String description) {
		super(description);
	}

}
