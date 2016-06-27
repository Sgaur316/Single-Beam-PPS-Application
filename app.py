import socket
import config
import projection

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.SERVER_IP, config.SERVER_PORT)
print 'connecting to %s port %s' % server_address
sock.connect(server_address)
print 'Connected to server...'

# Send connect packet with ID
data = "pps_id, %s" % config.PPS_ID
print "sending: ", data
res = sock.send(data)

def isFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

while True:
    print "Expecting a command from server..."
    msg = sock.recv(4096)
    msg = msg.strip()
    print "Received message:", msg
    if msg == 'stop':
        print "Stopping the projector"
        projection.display.stop()

    elif len(msg) >= 5 and msg[:5] == 'point':
        [X, Y, _D1, _D2, _D3, _BotDir] = [float(s) for s in msg.split(",") if isFloat(s)]
        print "Projector pointing to (X, Y)"
        projection.display.pointAndOscillate(X, Y)

    else:
        print "Unrecognized message from server"
