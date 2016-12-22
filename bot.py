import sys
import socket 
import select 
from chat_client import * 

HOST = 'localhost'
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009 


def chat_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST,PORT))
	server_socket.listen(10)
	SOCKET_LIST.append(server_socket)
	print "Chat server started on "+ str(PORT)
	while 1:
		# get the list sockets which are ready to be read through 
		# 4th arg time_out = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
		for sock in ready_to_read:
			# a new connection request received 
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				print "Client (%s %s) connected " %addr 
				broadcast(server_socket,sockfd, "[%s:%s] entered romm \n"%addr) 
			else:
				# process data from the socket
				try: 
					data = sock.recv(RECV_BUFFER)
					if data:
						# there is something in the socket
						print "calling mongo connect"
						mongo_handle = mongo_connect()
						collection_handle = mongo_handle['whatsapp']
						phone_no = data.split(":")[0]
						message_by_phone_no = data.split(":")[1] 
						print "Inserting data in database ",phone_no, message_by_phone_no
						collection_handle.chat.insert_one({phone_no:message_by_phone_no})
						print '['+str(sock.getpeername())+']'+data
						from socketIO_client import SocketIO, LoggingNamespace
						with SocketIO('localhost',8000,LoggingNamespace) as socketIO:
							socketIO.emit(data)
						broadcast(server_socket,sock,"\r" + '['+str(sock.getpeername())+']'+data)
					else:
						# remove the socket that is broken 
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)
						boradcast(server_socket,sock,"client (%s, %s) is offline \n"%addr)
				except Exception,e:
					print "Exception found while data has to socket",str(e)
					broadcast(server_socket, sock, "Client (%s, %s) is offline \n"%addr)
					continue 
	server_socket.close()


def broadcast(server_socket,sock,message):
	for socket in SOCKET_LIST:
		if socket != server_socket and socket != sock:
			try:
				socket.send(message)
			except:
				socket.close()
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)


if __name__ == "__main__":
	sys.exit(chat_server())


