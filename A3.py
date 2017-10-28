import socket
import socketserver
import sys
import threading
import time
import traceback

OUTGOING = "---->"
INCOMING = "<----"
TIMEZONE = None #timezone(US/Mountain) # Need to install pytz library

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
	HOST = "localhost"

	#Correct number of args check
	if len(sys.argv) < 7 and sys.argv[1] == "-replace":
		print("-not good enough replace args")
		sys.exit()
	elif len(sys.argv) < 8 and sys.argv[1] == "-log":
		print("-not good enough replace args")
		sys.exit()
	elif len(sys.argv) < 9 and len(sys.argv) > 3:

		#Check Commands
		"""
		This part is just getting the commands from the user
		Then it sets flags for replace and/or log 
		"""
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
		server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
		print("Listening to PORT: " + str(PORT))
		server.serve_forever()

	except Exception as e:
		print("An error occured: " + str(e))
		sys.exit()
