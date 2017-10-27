import socket
import SocketServer
import sys
import threading
import asyncore
import datetime
import requests
from pytz import timezone
import traceback

OUTGOING = "---->"
INCOMING = "<----"
MOUNTAIN = timezone(US/Mountain)

class MyTCPHandler(socketserver.BaseRequestHandler):
	CONNECTED = False                   # connection flag
	BUFFER_SIZE = 4096
	loggingCommands = ['-raw','-strip','-hex', '-autoN']

	"""
	REPLACE: Not Tested -------------------------------------------------------------------------------------------------------
	"""
	#Read response as a string, replace target string with replacement string
	def replacer(response, target, targetReplacement):
		response = str(response)
		target = str(target)
		targetReplacement = str(targetReplacement)
		response = response.replace(target, targetReplacement)
		return response

	"""
	LOGGING: Work in Progress ------------------------------------------------------------------------------------------------
	"""
	def logging(response, logCommand):
		response = response
		logCommand = logCommand
		if logCommand == "-raw":
			#
		elif logCommand == "-strip":
			#
		elif logCommand == "-hex":
			#
		elif logCommand == "-autoN":
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
		dateTime = datetime.now(MOUNTAIN) #Current Date + Time
		print("Connection from: " + self.client_address[0] + " @: " + dateTime)

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

		# Call commands here
		response = self.requests(srcPort, server, dstPort, data)

		if logFlag == True:
			self.logging(response, logCommand)
		if replaceFlag == True:
			self.replacer(response,target,targetReplacement)

		# Send out final response
		print(response)



"""
THIS IS STILL A2 CODE
"""
if __name__ == "__main__":
	HOST = "localhost"


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

		# Set flags initially to false
		logFlag = False 
		replaceFlag = False 

		# Get Essentials	
		dstPort = int(sys.argv[len(sys.argv) - 1])
		server = (sys.argv[len(sys.argv) - 2])
		srcPort = int(sys.argv[len(sys.argv) - 3])

		# Get check for logging or replacement flags
		if sys.argv[1] in self.loggingCommands:
			logFlag = True
			logCommand = sys.argv[1]
		if sys.argv[1] == "-replace" or sys.argv[2] == "-replace":
			replaceFlag = True
			target = (sys.argv[len(sys.argv) - 5]
			targetReplacement = (sys.argv[len(sys.argv) - 4]
		

	except:
		response = errorMessage
		tb = traceback.format_exc()
		print (tb)

	if len(sys.argv) > 1:
		PORT = int(sys.argv[1])
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
