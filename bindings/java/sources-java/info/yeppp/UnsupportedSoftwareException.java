/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

package info.yeppp;

/**
 * @brief	Unsupported software exception
 * @details	This exception is thrown when system software does not support the operations required by @Yeppp function call.
 */
public class UnsupportedSoftwareException extends RuntimeException {
	
	/**
	 * @brief	Constructs an unsupported software exception with the specified description.
	 */
	public UnsupportedSoftwareException(String description) {
		super(description);
	}

}
