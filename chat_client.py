import sys 
import socket 
import select 


def mongo_connect(): # TBD make it parameterized 
	from pymongo import MongoClient
	client = MongoClient()
	return client    #Db handle  
	

def check_registered(mobile_number='8123340865'):
	db_client = mongo_connect()
	database_connection = db_client['whatsapp']  # db instance 
	collection_doc = database_connection.user.find({"mobile_number":mobile_number}).count()
	if collection_doc > 0:
		return True          
	else:
		return False    # User not registered 

def chat_client():
	if(len(sys.argv) < 3):
		print "Usage : python chat_client.py hostname port"
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])
	print "client connecting to host and port ",host ,port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		s.connect((host,port))
	except Exception,e:
		print str(e)
		print "unable to connect"
		sys.exit()

	user_phone_number=str(raw_input("enter your 10 digit phone number : "))
	while(len(user_phone_number)!=10):   # basic check 
		print "please enter 10 digit mobile number"
		user_phone_number = str(raw_input("enter your 10 digit phone number : "))
	while not check_registered(user_phone_number):
		user_phone_number = str(raw_input("previous user was not registerd please enter your 10 digit phone number : "))

	user_phone_number = user_phone_number + " : "
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
					sys.stdout.write(user_phone_number); sys.stdout.flush()
			else:
				msg = sys.stdin.readline()
				s.send(user_phone_number + str(msg))
				sys.stdout.write(user_phone_number); sys.stdout.flush()

if __name__ == '__main__':
	sys.exit(chat_client())

