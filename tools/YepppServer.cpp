/*
 *     Daemon for access to energy counters without superuser privileges
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 * Author: rschoene
 */

// the port to listen to
#define YEPPP_PORT 17037
// exit if errors during accept
#define YEPPP_EXIT_ON_ACCEPT_FAILURE true
// close existing sockets before binding this
#define YEPPP_CLOSE_EXISTING false
// 1) if request.kind_counter equals this value, then the server should be closed
// 2) return value of handleRequest() if the server should be closed
#define HANDLE_REQUEST_SHOULD_END -2
// false to force exit on missing bytes while handling request
#define YEPPP_IGNORE_MISSING_BYTES_RECV true
// print extra messages?
#define YEPPP_VERBOSE true

// headers for network
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <unistd.h>

// standard headers
#if YEPPP_VERBOSE
#include <time.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// app headers
#include "yeppp_server.h"
#include <yepLibrary.h>


YepEnergyCounter former_state;

void closing(int socketfd, int exit_value) {
	// close existing socket
#if YEPPP_VERBOSE
	printf("Closing socket with fd=%d\n", socketfd);
#endif
	if(close(socketfd)) {
		// Error occured
		perror("Error during closing the existing socket: ");
		exit(EXIT_FAILURE);
	}
	exit(exit_value);
}

int handleRequest(int socketfd) {
	// read structure from client
	struct counter_data request;
	bzero(&request, sizeof(request));
	int sent_bytes, n;

	n = sizeof(request);
	sent_bytes = recv(socketfd, &request, n, 0);
	if(sent_bytes == 0) {
		// Server has shut down connection
		fprintf(stderr, "Client has shut down connection.\n");
		return EXIT_FAILURE;
	}
	else if(sent_bytes < 0) {
		// Error occured
		perror("Error during receiving: ");
		return EXIT_FAILURE;
	}
	else if(n - sent_bytes > 0) {
		fprintf(stderr, "Did not receive all ,just %d of %d bytes.\n", sent_bytes, n);
#if YEPPP_IGNORE_MISSING_BYTES_RECV
		fprintf(stderr, "Ignoring this warning.\n");
#else
		return EXIT_FAILURE;
#endif
	}

	Yep64u ticks;
	enum YepStatus status = yepLibrary_GetTimerTicks(&ticks);
	printf("getTimerTicks. retval=%d, ticks=%llu", status, ticks);
	// actually handle the request
	// check if the server should be closed (magic value)
	if(request.kind_counter == HANDLE_REQUEST_SHOULD_END) {
		printf("Got magic value to close server.\n");
		return HANDLE_REQUEST_SHOULD_END;
	}

	if(request.kind_counter == 0) {
		// release the counter and store the result
		double measure;
		enum YepStatus status = yepLibrary_GetEnergyCounterRelease(&former_state, &measure);
#if YEPPP_VERBOSE
		printf("Measured %f\n", measure);
#endif
		if(status == YepStatusOk) {
			// write result
			request.read_value = measure;
			request.error_code = 0;
		}
		else {
			request.read_value = -1;
			request.error_code = status;
		}
	}
	else {
		// kind_counter is indicating to acquire
		enum YepEnergyCounterType type;
		switch(request.kind_counter) {
		case 1:
			type = YepEnergyCounterTypeRaplPackageEnergy;
			break;
		case 2:
			type = YepEnergyCounterTypeRaplPowerPlane0Energy;
			break;
		default:
			type = YepEnergyCounterTypeRaplDRAMPower;
			break;
		}
		if(type == YepEnergyCounterTypeRaplDRAMPower) {
			// XXX considered as failure !
			fprintf(stderr, "Unknown type given: %d\n", request.kind_counter);
		}
		enum YepStatus status = yepLibrary_GetEnergyCounterAcquire(type, &former_state);
#if YEPPP_VERBOSE
		printf("Acquired for type %d.\n", type);
#endif
		request.read_value = 0;
		if(status == YepStatusOk) {
			request.error_code = 0;
		}
		else {
			request.error_code = status;
		}
	}

	// send request back (now with read_value filled out)
	sent_bytes = send(socketfd, &request, n, 0);
	if(sent_bytes < 0) {
		// Error occured
		perror("Error during sending: ");
		return EXIT_FAILURE;
	}
	else if(n - sent_bytes > 0) {
		// Did not sent all
		fprintf(stderr, "Did not receive all ,just %d of %d bytes.\n", sent_bytes, n);
		return EXIT_FAILURE;
	}

	if(close(socketfd)) {
		// Error occured
		perror("Error during closing the existing socket: ");
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}

int main(int argc, char **argv) {
	// initialize library
	enum YepStatus status = yepLibrary_Init();
	if(status != YepStatusOk) {
		fprintf(stderr, "Error while initializing Yeppp Library: %d\n", status);
		return EXIT_FAILURE;
	}

	// create socket
#if YEPPP_VERBOSE
	printf("Creating socket.\n");
#endif
	int socketfd = socket(AF_INET, SOCK_STREAM, 0);
//	int option_value  = 1;
//	if(setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR, &option_value, sizeof(option_value))) {
//		// errors on setting option
//		perror("Error during socket init (option SO_REUSEADDR): ");
//	}
	if(socketfd < 0) {
		perror("Error during socket init: ");
		return socketfd;
	}
#if YEPPP_VERBOSE
	printf("Socket created with fd=%d\n", socketfd);
#endif

#if YEPPP_CLOSE_EXISTING
	// close existing socket
	if(close(socketfd)) {
		// Error occured
		perror("Error during closing the existing socket: ");
		return EXIT_FAILURE;
	}
	socketfd = socket(AF_INET, SOCK_STREAM, 0);
#endif

	struct sockaddr_in server;
	bzero((char *) &server, sizeof(server));
	server.sin_family = AF_INET;
//	unsigned long addr = inet_addr(YEPPP_IP);
//	memcpy( (char*)&server.sin_addr, &addr, sizeof(addr));
	server.sin_addr.s_addr = INADDR_ANY; // maybe use INADDR_LOOPBACK
	server.sin_port = htons(YEPPP_PORT);

#if YEPPP_VERBOSE
	printf("Binding socket at <any_adress>:%d.\n", YEPPP_PORT);
#endif
	if(bind(socketfd, (struct sockaddr*) &server, sizeof(server)) < 0) {
		perror("Error during socket binding");
		closing(socketfd, EXIT_FAILURE);
	}

#if YEPPP_VERBOSE
	printf("Listening on socket.\n");
#endif
	// allow two clients (actually one would be enough)
	if(listen(socketfd, 2)) {
		perror("Error during listening: ");
		closing(socketfd, EXIT_FAILURE);
	}

	// enter endless loop
	while(true) {
		struct sockaddr_in client;
		socklen_t len = sizeof(client);
		int newsocketfd = accept(socketfd,  (struct sockaddr*) &client, &len);
		if(newsocketfd == -1) {
			perror("Error during accepting: ");
			if(YEPPP_EXIT_ON_ACCEPT_FAILURE) {
				closing(socketfd, EXIT_FAILURE);
			}
		}

#if YEPPP_VERBOSE
		time_t now;
		time(&now);
		// no newline needed (%s or ctime() handles this somehow)
		printf("Handling request from client (socket %d) at %s", newsocketfd, ctime(&now));
#endif
		int ret = handleRequest(newsocketfd);
		if(ret) {
			if(ret == HANDLE_REQUEST_SHOULD_END) {
				break;
			}
			fprintf(stderr, "Problems handling the request.\n");
		}
	}

	status = yepLibrary_Release();
	if(status != YepStatusOk) {
		fprintf(stderr, "Error while releasing Yeppp Library: %d\n", status);
	}
	// everything went fine with sockets
	closing(socketfd, EXIT_SUCCESS);
}
