import socket
import config
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.SERVER_IP, config.SERVER_PORT)
print 'connecting to %s port %s' % server_address
sock.connect(server_address)
print 'Connected to server...'


while True:
	print "Expecting a message from server..."
	time.sleep(2)