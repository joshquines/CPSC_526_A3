import socket
import socketserver
import sys
import threading
import time
import traceback


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

			
	DST_PORT = int(sys.argv[len(sys.argv) - 1])
	HOST = sys.argv[len(sys.argv) - 2]
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

"""
	#Correct number of args check
	if len(sys.argv) < 7 and sys.argv[1] == "-replace":
		print("-not good enough replace args")
		sys.exit()
	elif len(sys.argv) < 8 and sys.argv[1] == "-log":
		print("-not good enough replace args")
		sys.exit()
	elif len(sys.argv) < 9 and len(sys.argv) > 3:

		#Check Commands
		
		This part is just getting the commands from the user
		Then it sets flags for replace and/or log 
		
		errorMessage = "\n".join([
			"Input error.",
			"\nUsage: [logOptions] [replaceOptions] srcPort server dstPort",
			"\nlogOptions usage: [-raw, -strip, -hex, -autoN]",
			"\nreplaceOptions usage: -replace <target> <targetReplacement>"
			])

		try:
			global logFlag, replaceFlag, dstPort, server, srcPort, target, targetReplacement
			loggingCommands = ['-raw','-strip','-hex', '-autoN']

			# Set flags initially to false
			logFlag = False 
			replaceFlag = False 

			# Get Essentials	
			dstPort = int(sys.argv[len(sys.argv) - 1])
			server = (sys.argv[len(sys.argv) - 2])
			srcPort = int(sys.argv[len(sys.argv) - 3])
			PORT = srcPort

			# Get check for logging or replacement flags
			if sys.argv[1] in loggingCommands:
				logFlag = True
				logCommand = sys.argv[1]
				print("Running Log: " + str(logCommand))
			if sys.argv[1] == "-replace" or sys.argv[2] == "-replace":
				replaceFlag = True
				target = (sys.argv[len(sys.argv) - 5])
				targetReplacement = (sys.argv[len(sys.argv) - 4])
				print("Running replacement: " + str(target) + " replaced by: " + str(targetReplacement))

			

		except:
			response = errorMessage
			tb = traceback.format_exc()
			print (tb)
	else:
		print("Port number not specified.")
		print("Usage: python3 A2.py <port>\n")
		sys.exit()

	try:
		server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
		print("Listening to PORT: " + str(PORT))
		server.serve_forever()

	except Exception as e:
		print("An error occured: " + str(e))
		sys.exit()
"""