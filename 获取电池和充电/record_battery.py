import socket
import time
import datetime

#record battery and charging to a file every 10 seconds.

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/pcat-manager.sock")

t0= time.time()

f = open("battery_log.txt", "a")

while True:
    s.send(b"{'command':'pmu-status'}\0")
    data=s.recv(256).strip()
    now = datetime.datetime.now()
    tnow = time.time()
    passed= round(tnow - t0,1)
    out=(str(passed) + "|" + now.strftime("%Y-%m-%d %H:%M:%S") + "|" + data.decode())
    print(out)
    f.write(out+"\n")
    f.flush()
    time.sleep(10)


f.close()
