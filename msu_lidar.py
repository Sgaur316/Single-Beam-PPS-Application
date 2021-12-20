import socket
import threading
import logger
import json
from time import sleep
from config import (
    MSU_LIDAR_SERVICE_IP,
    MSU_LIDAR_SERVICE_PORT
)

logHandle = logger.logHandle

class Msu_lidar_client(object):
    def set_keep_alive_linux(self, sock, after_idle_sec=1, interval_sec=3, max_fails=5):
        """Set TCP keep alive on an open socket.

        It activates after 1 second (after_idle_sec) of idleness,
        then sends a keep alive ping once every 3 seconds (interval_sec),
        and closes the connection after 5 failed ping (max_fails), or 15 seconds
        """
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

    def start(self):
        self.t = threading.Thread(target=self.create_msu_lidar_client)
        self.t.start()

    def create_msu_lidar_client(self):
        while True:
            try:
                server_address = (MSU_LIDAR_SERVICE_IP, MSU_LIDAR_SERVICE_PORT)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if not self.sock:
                    logHandle.error("MSU lidar: Error in creating msu lidar socket connection, Retrying to connect after 5 sec")
                    sleep(5)
                    continue
                self.set_keep_alive_linux(self.sock)
                logHandle.info('MSU lidar: connecting to %s port %s' % server_address)
                self.sock.connect(server_address)
                logHandle.info('MSU lidar: Connected to msu lidar application...')
                while True:
                    logHandle.info("MSU lidar: Waiting for data reception on msu lidar...")
                    msg = self.sock.recv(4096)
                    if len(msg) == 0:
                        logHandle.info("MSU lidar: Network connection lost, Retrying to connect after 5 sec")
                        self.sock.close()
                        self.sock = None
                        sleep(5)
                        break
                    else:
                        logHandle.info("MSU lidar: Received message: %s" % msg)
            except Exception as e:
                logHandle.info("MSU lidar: Error %s closing socket and creating a new socket After 5 sec" % e)
                self.sock.close()
                self.sock = None
                sleep(5)
                continue

            except socket.timeout as e:
                logHandle.info("MSU lidar: Timeout Socket Error %s closing socket and creating a new socket After 5 sec" % e)
                self.sock.close()
                self.sock = None
                sleep(5)
                continue
    
    def send_data_to_msu_lidar_client(self, data):
        if not self.sock:
            return False
        if len(data) >= 5 and data[:5] == 'point':
            packet = {
                "process": "projector",
                "data": {
                    "projector_data": data
                }
            }
            try:
                logHandle.info("MSU lidar: sending points data packet to msu lidar client {}".format(packet))
                self.sock.send(json.dumps(packet).encode('utf-8'))
                return True
            except Exception as e:
                logHandle.error("MSU lidar: Exception while sending data to msu lidar client {}".format(e))
                return False
            
msu_lidar_client = Msu_lidar_client()
      