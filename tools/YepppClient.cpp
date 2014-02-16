/*
 *     Client to access to energy counters without superuser privileges
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 * Author: rschoene
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <stdio.h>
#include <stdlib.h>
#include "yeppp_client.h"

/**
 * Closes the socket and returns the given exit value.
 * If closing the socket fails, return #ERROR_CODE_CLOSING_SOCKET
 * @param[in] socketfd The file descriptor of the socket to close.
 * @param[in] exit_value
 */
int closing(int socketfd, int exit_value) {
	// close existing socket
	printf("Closing socket with fd=%d\n", socketfd);
	if(close(socketfd)) {
		// Error occured
		perror("Error during closing the existing socket: ");
		exit_value = ERROR_CODE_CLOSING_SOCKET;
	}
	return exit_value;
}

/**
 * Takes the request, sends it to the server and receive the response storing
 * it in the request.
 * For sending the request, only the kind_counter attribute is used.
 * On failure the received request has an error_code greater than zero and an
 * undetermined read_value. On success, the error_code is equal to zero and
 * the read_value equals to the value of the read counter.
 * @param[in/out] request The request to send. Will contain the received request as described above.
 * @retval #ERROR_CODE_CONNCECTION		Could not connect to the socket.
 * @retval #ERROR_CODE_SEND_GENERAL		Problems with sending the request.
 * @retval #ERROR_CODE_SEND_BYTES		Did not sent all bytes of the request.
 * @retval #ERROR_CODE_RECV_SHUTDOWN	The server socket has shut down the connection.
 * @retval #ERROR_CODE_RECV_GENERAL		Problems with receiving the response.
 * @retval #ERROR_CODE_RECV_BYTES		Did not receive all bytes of the response.
 * @retval #EXIT_SUCCESS				The response information was stored in the given request.
 */
int sendAndReceiveRequest(counter_data* request) {
	// create socket
	int socketfd = socket(AF_INET, SOCK_STREAM, 0);
	if(socketfd < 0) {
		perror("Error during socket init: ");
		return ERROR_CODE_INIT_SOCKET;
	}
	int option_value  = 1;
	if(setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR, &option_value, sizeof(option_value))) {
		// errors on setting option
		perror("Error during socket init (option SO_REUSEADDR): ");
	}

	// prepare connection
	struct sockaddr_in server;
	bzero((char *) &server, sizeof(server));

	unsigned long addr = inet_addr(YEPPP_IP);
	memcpy( (char*)&server.sin_addr, &addr, sizeof(addr));
	server.sin_family = AF_INET;
	server.sin_port = htons(YEPPP_PORT);

	// connect
	if(connect(socketfd, (struct sockaddr*)&server, sizeof(server)) == -1) {
		// Error occured
		perror("Error during connecting: ");
		return closing(socketfd, ERROR_CODE_CONNCECTION);
	}

	// send structure
	int n = sizeof(*request);
	int sent_bytes = send(socketfd, request, n, 0);
	if(sent_bytes == -1) {
		// Error occured
		perror("Error during sending: ");
		return closing(socketfd, ERROR_CODE_SEND_GENERAL);
	}
	else if(n - sent_bytes > 0) {
		// Did not sent all
		fprintf(stderr, "Did not sent all, just %d of %d bytes.\n", sent_bytes, n);
		return closing(socketfd, ERROR_CODE_SEND_BYTES);
	}

	// receive structure
	sent_bytes = recv(socketfd, request, n, 0);
	if(sent_bytes == 0) {
		// Server has shut down connection
		fprintf(stderr, "Server has shut down connection.\n");
		return closing(socketfd, ERROR_CODE_RECV_SHUTDOWN);
	}
	else if(sent_bytes == -1) {
		// Error occured
		perror("Error during receiving: ");
		return closing(socketfd, ERROR_CODE_RECV_GENERAL);
	}
	else if(n - sent_bytes > 0) {
		fprintf(stderr, "Did not receive all, just %d of %d bytes.\n", sent_bytes, n);
		return closing(socketfd, ERROR_CODE_RECV_BYTES);
	}

	// finally got the return value
	if(request->error_code > 0) {
		fprintf(stderr, "Received error code %d.", request->error_code);
		return closing(socketfd, request->error_code);
	}

	// everything went fine
	return closing(socketfd, EXIT_SUCCESS);
}

/**
 * Calls #sendAndReceiveRequest with either a value given as program argument,
 * or if no such on is given, read one from stdin.
 * Prints the result of the call to stdout.
 */
int main(int argc, char **argv) {
	struct counter_data request;
	//TODO let ip and port be specified as arguments

	// prepare structure
	// -2=close server, 0=release, 1-8=acquire this kind of counter
	if(argc > 1) {
		// counter type given by first argument
		request.kind_counter = atoi(argv[1]);
	}
	else {
		// read from stdin
		char buffer[256];
	#if YEPPP_CLIENT_VERBOSE
		printf("Enter number (-2=close server, 0=release, 1-8=acquire this kind of counter)\n");
	#endif
		bzero(buffer, 256);
		fgets(buffer, 255, stdin);
		request.kind_counter = atoi(buffer);
	}
	int retval = sendAndReceiveRequest(&request);
	printf("Retval: %d, kind_counter: %d, error_code: %d, read_value: %f\n",
			retval, request.kind_counter, request.error_code, request.read_value);
	return EXIT_SUCCESS;
}
