# -*- coding: utf-8 -*-

import socket
import time

import logger
import projection
import action_queue
from time import sleep

from config import (
    PPS_ID,
    SERVER_IP,
    SERVER_PORT
)

logHandle = logger.logHandle
server_address = (SERVER_IP, SERVER_PORT)


def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def set_keep_alive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keep alive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keep alive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


def main():
    while True:
        sock = create_socket()
        set_keep_alive_linux(sock)
        try:
            logHandle.info('App: connecting to %s port %s' % server_address)
            sock.connect(server_address)
            logHandle.info('App: Connected to server...')

            # Send connect packet with ID
            data = "pps_id, %s" % PPS_ID
            res = sock.send(bytes(data, 'utf-8'))
            projection.sender.start()
            while True:
                logHandle.info("App: Expecting a command from server...")
                msg = sock.recv(4096)
                if len(msg) == 0:
                    logHandle.info("App: Network connection lost, Retrying to connect after 5 sec")
                    sock.close()
                    projection.sender.stop()
                    action_queue.emptyQueue()
                    sleep(5)
                    break
                else:
                    msg = msg.decode().strip()
                    logHandle.info("App: Received message: %s" % msg)
                    action_queue.put(msg)
        except Exception as e:
            logHandle.info("App: Error %s closing socket and creating a new socket After 5 sec" % e)
            sock.close()
            projection.sender.stop()
            action_queue.emptyQueue()
            sleep(5)
            continue

        except socket.timeout as e:
            logHandle.info("App: Timeout Socket Error %s closing socket and creating a new socket After 5 sec" % e)
            sock.close()
            projection.sender.stop()
            action_queue.emptyQueue()
            sleep(5)
            continue


if __name__ == '__main__':
    main()
