import paramiko
import sys
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

password = sys.argv[1]
target_mobile_num = sys.argv[2]
message = sys.argv[3]

ssh.connect("172.16.0.1", username="root", port=22, password=password)

shell = ssh.invoke_shell()
shell.send('picocom -b 115200 /dev/ttyUSB3\n')
time.sleep(1)
print(shell.recv(10000).decode("utf8"))

shell.send('\r')
#shell.send('AT+QNWPREFCFG="mode_pref",AUTO\r')
shell.send('AT+CMGF=1\r')
time.sleep(1)
print(shell.recv(10000).decode("utf8"))
shell.send('AT+CSCS="GSM"\r')
time.sleep(1)
print(shell.recv(10000).decode("utf8"))
shell.send('AT+CMGS="+target_mobile_num+"\r')
time.sleep(1)
shell.send(message+'\r')
shell.send('\x1A') #ctrl z
shell.send('\x1B') #escape
time.sleep(3)
print(shell.recv(10000).decode("utf8"))

shell.send('\x01')
shell.send('\x11')
time.sleep(1)
print(shell.recv(10000).decode("utf8"))

ssh.close()
