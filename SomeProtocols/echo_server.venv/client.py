import socket

#creating the client socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect to the server :
client_socket.connect(("49.249.90.204",30313))
# sending data to the server :
client_socket.send("hi mr Server , this is a good connection".encode('utf-8'))
recieved:'str'=client_socket.recv(1024).decode()

# close the connection :
client_socket.close()

#
print(f"the server sent : {recieved}")

