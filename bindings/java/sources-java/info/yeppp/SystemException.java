/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * Operating System exception
 * <p>
 * This exception is thrown when a Yeppp! function call fails inside the OS kernel.
 */
public class SystemException extends RuntimeException {
	
	/**
	 * Constructs an Operating System exception with the supplied description.
	 */
	public SystemException(String description) {
		super(description);
	}

}
