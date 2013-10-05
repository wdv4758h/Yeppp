/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * Unsupported software exception
 * <p>
 * This exception is thrown when system software does not support the operations required by Yeppp! function call.
 */
public class UnsupportedSoftwareException extends RuntimeException {
	
	/**
	 * Constructs an unsupported software exception with the specified description.
	 */
	public UnsupportedSoftwareException(String description) {
		super(description);
	}

}
