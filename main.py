""" Main file basically acts as the initiation point and our client which maintains the contact with the server"""
# importing libraries
import socket
from source.projection import Display
from source import action_queue
from source.calibration import Calibration
from source import logger
from time import sleep
from config import SERVER_IP, SERVER_PORT, PPS_ID
import sys
import os

class Connection():
    server_address = (SERVER_IP, SERVER_PORT)
    logHandle = logger.logHandle

    """
    Connection class is to establish Client-Server connection
    """
    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_keep_alive_linux(self, sock, after_idle_sec=1, interval_sec=3, max_fails=5):
        """Set TCP keepalive on an open socket.

        It activates after 1 second (after_idle_sec) of idleness,
        then sends a keepalive ping once every 3 seconds (interval_sec),
        and closes the connection after 5 failed ping (max_fails), or 15 seconds
        """
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

    def connection(self):
        """
        connection function is used to establish the client-server connection & stores received data in action-queue

        """
        Display().start()
        while True:
            sock = self.create_socket()
            self.set_keep_alive_linux(sock=sock)
            try:
                self.logHandle.info('App: connecting to %s port %s' % self.server_address)
                sock.connect(self.server_address)
                self.logHandle.info('App: Connected to server...')

                # Send connect packet with ID
                data = "pps_id, %s" % PPS_ID
                sock.send(data.encode('utf-8'))
                while True:
                    self.logHandle.info("App: Expecting a command from server...")
                    msg = sock.recv(4096)
                    msg = msg.decode()
                    if len(msg) == 0:
                        self.logHandle.info("App: Network connection lost, Retrying to connect after 5 sec")
                        sock.close()
                        action_queue.put('stop')
                        action_queue.emptyQueue()
                        sleep(3)
                        break
                    else:
                        msg = msg.strip()
                        self.logHandle.info("App: Received message: %s" % msg)
                        self.logHandle.info("The length of message received %s" % len(msg))
                        action_queue.put(msg)
                        # TODO: below lines to be deleted
                        # time.sleep(0.02)
                        # input("Press Enter: ")
                        # action_queue.put("stop")
                        # sock.send("get_next".encode('utf-8'))


            except Exception as e:
                self.logHandle.info("App: Error %s closing socket and creating a new socket After 5 sec" % (e))
                sock.close()
                action_queue.put("stop")
                action_queue.emptyQueue()
                sleep(5)
                continue


# When running the application we call main function with two optional arguments for two different modes.
# i.e. calibration and the application mode
if __name__ == '__main__':
    con = Connection()
    cal = Calibration()
    if len(sys.argv) > 2:
        sleep(1)
        os._exit(os.EX_OK)
    if len(sys.argv) == 2 and sys.argv[1] == "cal_mode":
        cal.calibrate()
    else:
        con.connection()