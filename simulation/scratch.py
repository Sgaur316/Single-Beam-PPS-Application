import socket
import sys
import random
# from config import SERVER_IP, SERVER_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
# server_address = (SERVER_IP, SERVER_PORT)
server_address = ("127.0.0.1", 9000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)

""" Coords Variable here imitates the actual server environment and sends coordinates to be pointed at in cms."""
# coords = ["18,9,2,0,0,0", "18,38,2,0,0,0", "18,57,2,0,0,0", "18,78,2,0,0,0", "18,112,0,0,0,0","18,132,0,0,0,0",
#           "18,150,0,0,0,0", "18,168,0,0,0,0", "18,187,0,0,0,0", "49,9,0,0,0,0", "49,38,0,0,0,0","49,57,0,0,0,0","49,78,0,0,0,0","49,112,0,0,0,0","49,132,0,0,0,0","49,150,0,0,0,0","49,168,0,0,0,0","49,187,0,0,0,0", "81,9,0,0,0,0", "81,38,0,0,0,0","81,57,0,0,0,0","81,78,0,0,0,0","81,112,0,0,0,0","81,132,0,0,0,0","81,150,0,0,0,0","81,168,0,0,0,0","81,187,0,0,0,0"]
# coords = ["11,3,0,0,0,0","25,3,0,0,0,0","42,3,0,0,0,0","57,3,0,0,0,0","74,3,0,0,0,0","88,3,0,0,0,0",
#           "11,22,0,0,0,0","25,22,0,0,0,0","42,22,0,0,0,0","57,22,0,0,0,0","74,22,0,0,0,0","88,22,0,0,0,0",
#           "11,38,0,0,0,0","25,38,0,0,0,0","42,38,0,0,0,0","57,38,0,0,0,0","74,38,0,0,0,0","88,38,0,0,0,0",
#           "11,55,0,0,0,0","25,55,0,0,0,0","42,55,0,0,0,0","57,55,0,0,0,0","74,55,0,0,0,0","88,55,0,0,0,0",
#           "11,71,0,0,0,0","25,71,0,0,0,0","42,71,0,0,0,0","57,71,0,0,0,0","74,71,0,0,0,0","88,71,0,0,0,0",
#           "11,104,0,0,0,0","25,104,0,0,0,0","42,104,0,0,0,0","57,104,0,0,0,0","74,104,0,0,0,0","88,104,0,0,0,0",
#           "11,120,0,0,0,0","25,120,0,0,0,0","42,120,0,0,0,0","57,120,0,0,0,0","74,120,0,0,0,0","88,120,0,0,0,0",
#           "11,136,0,0,0,0","25,136,0,0,0,0","42,136,0,0,0,0","57,136,0,0,0,0","74,136,0,0,0,0","88,136,0,0,0,0",
#           "11,153,0,0,0,0","25,153,0,0,0,0","42,153,0,0,0,0","57,153,0,0,0,0","74,153,0,0,0,0","88,153,0,0,0,0"]
# coords = ["0,0,8,0,0,-1", "98,0,8,0,0,-1", "0,210,8,0,0,-1", "98,210,8,0,0,-1", "49,9,8,0,0,-1", "98,100,8,0,0,-1",
          # "49,210,8,0,0,-1", "0,100,8,0,0,-1"]
# coords = ["18,9,2,2,0,0","81,9,2,2,0,0","0,100,2,2,0,0","49,0,2,2,0,0","18,185,2,2,0,0","81,185,0,2,0,0"]
coords = ["15,47,0,0,0,0","47,47,0,0,0,0","77,47,0,0,0,0", "109,47,0,0,0,0", "15,182,0,0,0,0","47,182,0,0,0,0","77,182,0,0,0,0", "109,182,0,0,0,0","30,13,0,0,0,0", "95,13,0,0,0,0"]

while True:
    print(sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print(sys.stderr, 'client connected:', client_address)
        index = 0
        while True:
            data = connection.recv(1024)
            data = data.decode('utf-8')
            print("received ", data)

            # 'point' string concatenation to be removed before release
            Deta = 'point,'+coords[random.randint(0, len(coords)-1)]
            if data == "ppsID":
                print("match")
                connection.sendall(Deta.encode('utf-8'))

            elif data == "get_next":
                # connection.send("stop".encode('utf-8'))
                # time.sleep(0.2)
                Deta = 'point,' + coords[random.randint(0, len(coords)-1)]
                connection.send(Deta.encode('utf-8'))

            else:
                break
    finally:
        connection.close()