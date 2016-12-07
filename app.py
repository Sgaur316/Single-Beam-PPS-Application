import socket
import config
import projection
from time import sleep
import threading
import actionQueue
import logger


logHandle = logger.logHandle
server_address = (config.SERVER_IP, config.SERVER_PORT)


def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def set_keep_alive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
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
            data = "pps_id, %s" % config.PPS_ID
            res = sock.send(data)
            projection.sender.start()
            while True:
                logHandle.info("App: Expecting a command from server...")
                msg = sock.recv(4096)  
                if len(msg) == 0:
                    logHandle.info("App: Network connection lost, Retrying to connect after 5 sec")
                    sock.close()
                    projection.sender.stop()
                    actionQueue.emptyQueue()
                    sleep(5)
                    break
                else:
                    msg = msg.strip()
                    logHandle.info("App: Received message: %s" % msg)
                    actionQueue.put(msg)                    
        except Exception, e:
            logHandle.info("App: Error %s closing socket and creating a new socket After 5 sec" % (e))
            sock.close()
            projection.sender.stop()
            actionQueue.emptyQueue()
            sleep(5)
            continue

if __name__ == '__main__':
    main()
