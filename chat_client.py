import sys 
import socket 
import select 

def chat_client():
	if(len(sys.argv) < 3):
		print "Usage : python chat_client.py hostname port"
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])
        print "client connecting to host %s and port %s ",host , port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		s.connect((host,port))
	except Exception,e:
                print str(e)
		print "unable to connect"
		sys.exit()
	while 1:
		socket_list = [sys.stdin,s ]
		# Get the list sockets which are readable 
		ready_to_read, ready_to_write, in_error = select.select(socket_list,[],[])
		for sock in ready_to_read:
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print "Disconeected from chat server"
					sys.exit()
				else:
					# print data
					sys.stdout.write(data)
					sys.stdout.write('[ME]'); sys.stdout.flush()
			else:
				msg = sys.stdin.readline()
				s.send(msg)
				sys.stdout.write('[Me]'); sys.stdout.flush()

if __name__ == '__main__':
	sys.exit(chat_client())

