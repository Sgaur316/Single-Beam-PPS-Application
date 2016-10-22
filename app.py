import socket
import config
import projection
from logger import gorLogger
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.SERVER_IP, config.SERVER_PORT)
gorLogger.loggerInit('projector','projector.log','./log')
logHandle = gorLogger.getInstance()
logHandle.info('\n<<<<<<<<<< Projector Started >>>>>>>>>>\n')
def isFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

while True:
    try:
        logHandle.info('connecting to %s port %s' % server_address)
        sock.connect(server_address)
        logHandle.info('Connected to server...')

        # Send connect packet with ID
        data = "pps_id, %s" % config.PPS_ID
        logHandle.info("sending data: %s" % data)
        res = sock.send(data)

        while True:
            logHandle.info("Expecting a command from server...")
            msg = sock.recv(4096)
            msg = msg.strip()
            logHandle.info("Received message: %s" % msg)
            if msg == 'stop':
                logHandle.info("Stopping the projector")
                projection.display.stop()
            elif len(msg) >= 5 and msg[:5] == 'point':
                [X, Y, _D1, _D2, _D3, _BotDir] = [float(s) for s in msg.split(",") if isFloat(s)]
                logHandle.info("Projector pointing to {%s,%s}"% (X,Y))
                retMsg = projection.display.pointAndOscillate(X, Y)
                logHandle.info(retMsg)
            else:
                logHandle.info("Unrecognized message from server, terminating")
                sock.close()
                break

    except Exception, e:
        logHandle.info("Error %s retrying in 5 seconds" % (e))
        sleep(5)
        continue         
