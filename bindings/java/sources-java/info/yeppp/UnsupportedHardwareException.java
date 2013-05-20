/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

package info.yeppp;

/**
 * @brief	Unsupported hardware exception
 * @details	This exception is thrown when system lacks hardware required for the requested @Yeppp function call.
 */
public class UnsupportedHardwareException extends RuntimeException {
	
	/**
	 * @brief	Constructs an unsupported hardware exception with the specified description.
	 */
	public UnsupportedHardwareException(String description) {
		super(description);
	}

}
