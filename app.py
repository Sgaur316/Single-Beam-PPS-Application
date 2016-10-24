import socket
import config
import projection
from time import sleep
import threading
import actionQueue
from logger import gorLogger
gorLogger.loggerInit('App','projector.log','./log')
logHandle = gorLogger.getInstance()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.SERVER_IP, config.SERVER_PORT)
logHandle.info('\n<<<<<<<<<< Projector Started >>>>>>>>>>\n')
def isFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

while True:
    try:
	logHandle.info('App: connecting to %s port %s' % server_address)
        sock.connect(server_address)
        logHandle.info('App: Connected to server...')

        # Send connect packet with ID
        data = "pps_id, %s" % config.PPS_ID
        logHandle.info("App: sending data: %s" % data)
        res = sock.send(data)
	projectionThread = threading.Thread(target=projection.start)
        projectionThread.start()
        while True:
            logHandle.info("App: Expecting a command from server...")
            msg = sock.recv(4096)    
            msg = msg.strip()
            logHandle.info("App: Received message: %s" % msg)
            actionQueue.put(msg)

    except Exception, e:
        logHandle.info("App: Error %s retrying in 5 seconds" % (e))
        sleep(5)
        continue
