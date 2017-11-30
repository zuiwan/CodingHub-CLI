# coding=UTF-8
import docker,sys
import threading
import time
import sys
BASE_URL='106.15.224.56:20120'
CONTAINERID='4afc59bf4c781e05f567d673058ee15145c587205c6b833ef5bbb9212c86583e'

def Send(socket):#发送消息
    while True:
		data = raw_input()
		socket.send(data+'\r')
def Recv(socket):#接收消息
	#while True:
		#data = socket.recv(1024)
		yy=socket.recv(1024)
		while True:
			buf = socket.recv(1024)
			if not len(buf):
				break
			# if isinstance(buf,gbk):
			#     print buf.decode('UTF-8', 'ignore').encode('gb2312')
		#data.decode('UTF-8', 'ignore')
		#print data
client = docker.DockerClient(base_url=BASE_URL,version='1.24',timeout=30)
execid=client.exec_create(container=CONTAINERID,cmd="/bin/sh",stdin=True,tty=True,privileged=True)
t = client.exec_start(execid,tty=True, stream=True, socket=True)
threads = []
t1 = threading.Thread(target=Send,args=(t,))
threads.append(t1)
t2 = threading.Thread(target=Recv,args=(t,))
threads.append(t2)
for k in threads:
	k.setDaemon(True)
	k.start()
k.join()
t.close()