/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * Misaligned pointer error
 * <p>
 * This exception is thrown when a pointer passed to Yeppp! function is not properly aligned.
 */
public class MisalignedPointerError extends Error {
	
	/**
	 * Constructs a misaligned pointer error with the specified description.
	 */
	public MisalignedPointerError(String description) {
		super(description);
	}

}
