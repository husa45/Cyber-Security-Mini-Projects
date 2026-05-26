import paramiko
import time
try:
    # establishing the connection
    client=paramiko.SSHClient()
    client.load_system_host_keys('/home/hussam/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect('127.0.0.1',username='ssh_user',password='1362004')
    #now openning the channel for interactive shell :
    channel=client.get_transport().open_session() # openning an interactive session
    channel.get_pty()
    shell=client.invoke_shell(term='xterm-256color')  #invoking a shell (default shell found in /etc/passwd

    while True:
            command=input("$ ")
            if command=='exit':
                break
            shell.sendall(command)
            now,output="f",''
            # while now:
            #     now=shell.recv(4096).decode()
            output=shell.recv(4096).decode()
            print(output)

  # stdin=channel.makefile_stdin('wb')
  #   stdout = channel.makefile_stdin('r')
  #   stdin.write('ls'.encode())
  #   stdin.flush()
  #   print(stdout,end="")
  #   print("d")






except paramiko.SSHException as ssh:
    raise SystemExit(ssh)
except KeyboardInterrupt:
    pass
