import paramiko
username=input("enter user name!!\n").strip()
try:
    client=paramiko.SSHClient()
    client.load_system_host_keys('/home/hussam/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect('127.0.0.1',port=22,username=username,password='123')
    print(f"logged in successfully to {username}")

    while True:
        try:
            command=input("$ ")
            if command=='exit':break
            stdin,stdout,stderr=client.exec_command(command)
            print(stdout.read().decode())
            erorr=stderr.read()
            if erorr:
                print(erorr)
        except KeyboardInterrupt:
            break

        except paramiko.SSHException as ssh:
            raise SystemExit(ssh)
        stdin.close()
        stdout.close()
        stderr.close()

except paramiko.SSHException:
    pass
print("transporting a file ")
sftp=client.open_sftp()
#sftp.
client.close()