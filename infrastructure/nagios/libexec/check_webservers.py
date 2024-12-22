#!/usr/bin/env python3

import sys
import socket
import logging

# Nagios exit codes
NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3

# File containing webserver list
WEBSERVERS_FILE = "/opt/nagios/etc/webservers.txt"
DEFAULT_TIMEOUT = 5  # Default timeout for server checks

# Configure logging
logging.basicConfig(level=logging.INFO)


def check_server(host, port, timeout):
    """Check if a server is reachable on a specific port."""
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, socket.gaierror):
        return False


def main():
    timeout = DEFAULT_TIMEOUT

    try:
        with open(WEBSERVERS_FILE, "r") as f:
            servers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"UNKNOWN - File {WEBSERVERS_FILE} not found")
        sys.exit(NAGIOS_UNKNOWN)

    if not servers:
        print(f"UNKNOWN - No servers listed in {WEBSERVERS_FILE}")
        sys.exit(NAGIOS_UNKNOWN)

    down_servers = []

    for server in servers:
        try:
            host, port = server.split(":")
            logging.info(f"Checking {host}:{port} with timeout {timeout}")
            if not check_server(host, port, timeout=timeout):
                down_servers.append(server)
        except ValueError:
            print(f"UNKNOWN - Invalid server format: {server}")
            sys.exit(NAGIOS_UNKNOWN)

    total_servers = len(servers)
    down_count = len(down_servers)

    if down_count == 0:
        print(f"OK - All {total_servers} servers are online")
        sys.exit(NAGIOS_OK)
    elif down_count == 1:
        print(f"WARNING - 1 server is offline: {down_servers[0]}")
        sys.exit(NAGIOS_WARNING)
    elif down_count == total_servers:
        print(f"CRITICAL - All servers are offline: {', '.join(down_servers)}")
        sys.exit(NAGIOS_CRITICAL)
    else:
        print(
            f"WARNING - {down_count}/{total_servers} servers are offline: {', '.join(down_servers)}"
        )
        sys.exit(NAGIOS_WARNING)


if __name__ == "__main__":
    main()
