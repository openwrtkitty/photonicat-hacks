import paramiko
import sys
import time

#used some script from lock4G/5G. use AT commands to query info.
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

password = sys.argv[1]
ret={}

ssh.connect("172.16.0.1", username="root", port=22, password=password)

shell = ssh.invoke_shell()

def sendcmd(cmd):
    shell.send(cmd)
    time.sleep(0.3)
    resp=shell.recv(10000).decode("utf8")
    print(resp)
    return resp


shell.send('picocom -b 115200 /dev/ttyUSB3\n')
time.sleep(0.3)
dummy=(shell.recv(10000).decode("utf8"))


imei_resp = sendcmd("AT+CGSN\r")
ret["imei"]=imei_resp.split("\n")[1].strip()

simnum_resp=sendcmd('AT+CNUM\r')
ret["simnum"]=simnum_resp.split("\n")[1].strip()

signal_resp=sendcmd('AT+CSQ\r')
ret["signal"]=signal_resp.split("\n")[1].strip()

netinfo_resp=sendcmd('AT+QNWINFO\r')
ret["netinfo"]=netinfo_resp.split("\n")[1].strip()

neighbour_resp=sendcmd('AT+QENG="servingcell"\r')
ret["neighbour"]=neighbour_resp.split("\n")[1].strip()

reject_resp=sendcmd('AT+QREJINFO\r')
ret["rej"]=reject_resp.split("\n")[1].strip()

spn_resp=sendcmd('AT+QSPN\r')
ret["spn"]=spn_resp.split("\n")[1].strip()

#maybe process later
#readsms_resp=sendcmd('AT+CMGL\r')
#ret["readsms"]=readsms_resp.split("\n")[1].strip()


shell.send('\x01')
shell.send('\x11')
time.sleep(1)
#print(shell.recv(10000).decode("utf8"))

ssh.close()
print(ret)
