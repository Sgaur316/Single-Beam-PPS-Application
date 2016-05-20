import socket
import config
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.SERVER_IP, config.SERVER_PORT)
print 'connecting to %s port %s' % server_address
sock.connect(server_address)
print 'Connected to server...'

time.sleep(0.5)
# Send connect packet with ID
data = "pps_id, %s" % config.PPS_ID
print "sending: ", data
res = sock.send(data)

while True:
    print "Expecting a message from server..."
    msg = sock.recv(4096)
    print "Received message: ", msg
    sock.send("abcd".encode())
    time.sleep(2)
