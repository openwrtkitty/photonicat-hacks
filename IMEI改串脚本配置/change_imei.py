import paramiko
import sys
import time

ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

password = sys.argv[1] 
imei = sys.argv[2] 

# 建立连接
ssh.connect("172.16.0.1", username="root", port=22, password=password)

shell = ssh.invoke_shell()
shell.send('picocom -b 115200 /dev/ttyUSB3\n')
time.sleep(1)
print(shell.recv(10000).decode("utf8"))

shell.send('\r')
shell.send(f'AT+EGMR=1,7,"{imei}"\r')
shell.send('\r')
time.sleep(3)
print(shell.recv(10000).decode("utf8"))

shell.send('\x01')
shell.send('\x11')
time.sleep(1)
print(shell.recv(10000).decode("utf8"))

# 关闭连接
ssh.close()
