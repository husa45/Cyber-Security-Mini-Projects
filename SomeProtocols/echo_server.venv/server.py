import socket
# create the socket :
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# bind it to an ip adress and port :
ipv4_addr,port="192.168.1.17",9999
server_socket.bind((ipv4_addr,port))
#listen for tcp connections on port 9999 :
server_socket.listen()
# accept tcp connection (stop executing until a connection is establishing )
client_socket,addr=server_socket.accept()
print(f"connection recieved from {addr}")

#recieving from the user , and echoing back what he has sent :
while True:
    recieved=client_socket.recv(1024).decode('utf-8')
    if not recieved:
        break
    client_socket.sendall(recieved.encode('utf-8'))

#closing the sockets :
server_socket.close()
client_socket.close()
