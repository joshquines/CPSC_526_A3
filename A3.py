import socket
import socketserver
import sys
import threading
import time
import traceback

#GLOBAL VARIABLES
OUTGOING = "---->"
INCOMING = "<----"
SRC_PORT = 0
HOST = ''
DST_PORT = 0
LOG_OPTIONS = ['-raw', '-strip', '-hex', '-auto32']
LOG_FLAG = False
LOG_COMMAND = 'none'
REPLACE_FLAG = False
ORIGINAL_T = ''
REPLACE_T = ''


class MyTCPHandler(socketserver.BaseRequestHandler):
	CONNECTED = False                   # connection flag
	BUFFER_SIZE = 4096


	"""
	REPLACE: Not Tested -------------------------------------------------------------------------------------------------------
	"""
	#Read response as a string, replace target string with replacement string
	def replacer(data, response, target, targetReplacement):
		"""Might have to change this to deal with bytearray instead of string"""
		data = data
		response = str(response)
		target = str(target)
		targetReplacement = str(targetReplacement)
		response = response.replace(target, targetReplacement)
		return response

	"""
	LOGGING: Work in Progress ------------------------------------------------------------------------------------------------
	"""
	def logging(data, response, logCommand):
		data = data.split(b'\r\n')
		response = response.split(b'\r\n')
		logCommand = logCommand
		if logCommand == "-raw":
			for line in data:
				print(OUTGOING, end="")
				for x in line:
					print(chr(x), end="")
			for line in response:
				print(INCOMING, end="")
				for x in line:
					print(chr(x), end="")

		elif logCommand == "-strip":
			for line in data:
				print(OUTGOING, end="")
				for x in line:
					#ADD CHECK IF PRINTABLE CHR HERE
					"""if x not printable, char = x"""
					print(chr(x), end="")
			for line in response:
				print(INCOMING, end="")
				for x in line:
					print(chr(x), end="")
		elif logCommand == "-hex":
			deletethis = 1
			#
		elif logCommand == "-autoN":
			deletethis = 1
			#



	#CONNECT TO REMOTE SERVER
	"""
	REQUESTS: Work in Progress -----------------------------------------------------------------------------------------------
	"""
	def requests(srcPort, server, dstPort):
		#CREATE TCP/IP SOCKET
		# https://docs.python.org/3/howto/sockets.html
		remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		remoteSocket.connect(server, dstPort)

	"""
	HANDLE: ------------------------------------------------------------------------------------------------------------------
	"""
	# MAIN FUNCTION HERE
	def handle(self):
    	
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)			# Create a socket object
    	serverSocket.bind((HOST, SRC_PORT))
   	 	serverSocket.listen(5)

		while True:
    		client, client_addr = serverSocket,accept()
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_socket.connect((SERVER, DST_PORT))
    	"""
		#Receive data from user
		self.CONNECTED = True
		timeNow = time.strftime("%a %b %d %H:%M:%S")
		print("New Connection: " + timeNow + ", from " + self.client_address[0])

		while self.CONNECTED:
			data = self.request.recv(self.BUFFER_SIZE)
			# Check the input
			if len(data) == self.BUFFER_SIZE:
				while 1:
					try: # Error means no more data
						data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
					except:
						break
			if len(data) == 0:
				break 
			data = data.decode("utf-8")

		#OPEN REMOTE SOCKET HERE

		# Call commands here, get initial response
		#response = self.requests(srcPort, server, dstPort, data)

		# Replace, log
		#if logFlag == True:
		#	self.logging(data, response, logCommand)
		#if replaceFlag == True:
		#	self.replacer(data, response,target,targetReplacement)

		# Send out final response
		#print(response)

		"""

"""
THIS IS STILL A2 CODE
"""
if __name__ == "__main__":
		
	if len(sys.argv) < 4 or len(sys.argv) == 6 or len(sys.argv) > 8 : 	# Minimum number of arguments is 3, maximum is 7
																		#Impossible to have ./A2.py + 5 arguments
		print("\nIncorrect number of parameters: ")
		print("Usage: ./A3.py [logOptions] [replaceOptions] srcPort server dstPort")
		print("[logOptions] and [replaceOptions] are optional parameters")
		print("[replaceOptions] takes in 2 parameters\n")
		sys.exit(0)
	elif len(sys.argv) == 5: #logOptions is always first arg
		if sys.argv[1] in LOG_OPTIONS:
			LOG_FLAG = True
			LOG_COMMAND = sys.argv[1]
			#print("Log command = " + LOG_COMMAND)
		else: #user wrote something over than a logOption
			print("\nIncorrect Usage of Logging Program: ")
			print("Usage: ./A3.py [logOptions] [replaceOptions] srcPort server dstPort")
			print("[logOptions] and [replaceOptions] are optional parameters")
			print("[replaceOptions] takes in 2 parameters\n")
			sys.exit(0)
	else: # More than 4 arguments, logoPtion is always first arg
		if sys.argv[1] in LOG_OPTIONS:
			LOG_FLAG = True
			LOG_COMMAND = sys.argv[1]
			print("Log command = " + LOG_COMMAND)

	HOST = "localhost"
	DST_PORT = int(sys.argv[len(sys.argv) - 1])
	SERVER = sys.argv[len(sys.argv) - 2]
	SRC_PORT = int(sys.argv[len(sys.argv) - 3])

	if '-replace' in sys.argv: # if -replace is an argument
		REPLACE_FLAG = True
		replaceIndex = sys.argv.index('-replace')
		print("found replace at index: " + str(replaceIndex))
		ORIGINAL_T = sys.argv[replaceIndex + 1]
		REPLACE_T = sys.argv[replaceIndex + 2]
		if ORIGINAL_T == str(SRC_PORT) or REPLACE_T == str(SRC_PORT):
			print("\nIncorrect Usage of -replace  ")
			print("Usage: ./A3.py [logOptions] [replaceOptions] srcPort server dstPort")
			print("[logOptions] and [replaceOptions] are optional parameters")
			print("[replaceOptions] takes in 2 parameters\n")
			sys.exit(0)
	
	#print(ORIGINAL_T,REPLACE_T)

	print("Port logger running: srcPort=" + str(SRC_PORT) + " host=" + HOST + " dstPort=" + str(DST_PORT))
	#print("Log command = " + LOG_COMMAND)

	server = socketserver.ThreadingTCPServer((HOST, SRC_PORT), MyTCPHandler)
	server.serve_forever()
