import socket
import SocketServer
import sys
import threading
import asyncore
import datetime
from pytz import timezone

OUTGOING = "---->"
INCOMING = "<----"
MOUNTAIN = timezone(US/Mountain)

class ProxyServer():

	loggingCommands = ['-raw','-strip','-hex', '-autoN']


	def replace():

	def logging():

	def requests(srcPort, server, dstPort):


	# MAIN FUNCTION HERE
	def handle(self):

		#Current Date + Time
		dateTime = datetime.now(MOUNTAIN)

		#CONNECTION
		print("Connection from: " + self.client_address[0] + " @: " + dateTime)

		# Taken from Assignment 2 
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
			print("%s wrote: %s" % (self.client_address[0], data.strip()))
			self.inputActions(data)
		# End Taken from Assignment 2

		# Connect to Remote Server



		#Check Commands
		errorMessage = "Please try again. Correct input is..... "
		"""
		LOL dammit the sys.argv[] = x is backwards
		"""
		try:
			if sys.argv[1] in self.loggingCommands: #If logging enabled
				if sys.argv[2] == "-replace": #If replace with logging
					sys.argv[1] = logCommand
					sys.argv[3] = target
					sys.argv[4] = targetReplacement
					sys.argv[5] = srcPort
					sys.argv[6] = server
					sys.argv[7] = dstPort
					#CALL REQUEST FUNCTION
					response = self.requests(srcPort, server, dstPort)
					#CALL REPLACE FUNCTION
					response = self.replace(response, target, targetReplacement)
					#CALL LOGGING FUNCTION
					response = self.logging()
					
				else:
					sys.argv[1] = logCommand
					sys.argv[4] = srcPort
					sys.argv[5] = server
					sys.argv[6] = dstPort
					#CALL REQUEST FUNCTION
					response = self.requests(srcPort, server, dstPort)
					#CALL LOGGING FUNCTION
					response = self.logging()

			elif sys.argv[1] == "-replace": #Replace only; no logging
				sys.argv[2] = target
				sys.argv[3] = targetReplacement
				sys.argv[4] = srcPort
				sys.argv[5] = server
				sys.argv[6] = dstPort
				#CALL REQUEST FUNCTION
				response = self.requests(srcPort, server, dstPort)
				#CALL REPLACE FUNCTION
				response = self.replace(response, target, targetReplacement)

			elif len(sys.argv) == 4: #No logging and replace
				sys.argv[1] = srcPort
				sys.argv[2] = server
				sys.argv[3] = dstPort
				#CALL REQUEST FUNCTION
				response = self.requests(srcPort, server, dstPort)
			else:
				response = errorMessage

			print(response)
		except:
			print(errorMessage)

"""
THIS IS STILL A2 CODE
"""
if __name__ == "__main__":
	HOST = "localhost"
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
