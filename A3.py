import socket
import socketserver
import sys
import threading
import time
import traceback
import select
import string

#GLOBAL VARIABLES
OUTGOING = "---->"
INCOMING = "<----"
SRC_PORT = 0
HOST = ''
DST_PORT = 0
LOG_OPTIONS = ['-raw', '-strip', '-hex']
LOG_FLAG = False
LOG_COMMAND = ''
REPLACE_FLAG = False
ORIGINAL_T = ''
REPLACE_T = ''
AUTONUM = 0

"""
Find ORIGINAL_T in data and replace with REPLACE_T
"""
def replacer(data):
	original = ORIGINAL_T.encode()
	replacement = REPLACE_T.encode()
	response = data.replace(original, replacement)
	return response


def logging(data, prefix):
	#RAW
	if LOG_COMMAND == "-raw":
		data = data.split(b'\n')
		#print("DEBUG: raw log")
		for line in data:
    		#decode each line in data and print
			line = line.decode("utf-8")
			print(prefix + " " +  str(line))

	#STRIP
	elif LOG_COMMAND == "-strip":
		data = data.split(b'\n')
		#print("DEBUG: strip log")
		for line in data:
    		# decode each line in data
			line= line.decode("utf-8")
			lineString = str(line)
			# replace byte if not printable
			for x in lineString:
				if not(x in string.printable):
					lineString = lineString.replace(x, ".")			
			print(prefix + " " + lineString)

	#HEXDUMP
	elif LOG_COMMAND == "-hex":
		data = data.split(b'\n')
		#print("DEBUG: hex log")
		for line in data:
			line = line.decode("utf-8")
			lineString = str(line)
			# get hex value of each character and replace the original character with its hex value in each line
			for x in lineString:
				hx = ":".join("{:02x}".format(ord(c)) for c in x)
				lineString = lineString.replace(x,hx)
			print(prefix + " " + lineString)

	#AUTON
	elif LOG_COMMAND == "-autoN":
		#print("DEBUG: autoN log")
		# split data into chunks of AUTONUM size
		chunks = [data[i:i + AUTONUM] for i in range(0, len(data), AUTONUM)]
		for x in chunks:
			xString = str(x)
			# see which characters to replace or print raw
			for y in x:
				y = chr(y)
				bitValue = ord(y)
				if bitValue == 9:
					yString == "\t"
				elif bitValue == 92:
					yString == "\\\\"
				elif bitValue == 10:
					yString == "\n"
				elif bitValue == 13:
					yString == "\r"
				elif bitValue < 32 or bitValue >127:
					yString = "\\" + str(bitValue)
				else:
					yString = str(y)
				xString = xString.replace(y, yString)
			print(prefix + xString[2:])
		
def clientHandler(client, dstSocket):
	inputs = [client, dstSocket]
	while 1:
		readable, writeable, exceptional = select.select(inputs, [], [])
		for sock in readable:
			data = sock.recv(1024)
			logData = data
			# If no data, close the current connection socket.
			if not data:
				print("No data provided. Connection closed.")
				client.close()
				dstSocket.close()
				return

			# If socket sending data is the destination socket send the data to the client
			if sock == dstSocket:
				if REPLACE_FLAG == True:
					logData = replacer(data)

				if LOG_FLAG == True:
					logging(logData, INCOMING)

				client.sendall(data)
			# Otherwise send the data from client to the destination
			else:
				if REPLACE_FLAG == True:
					logData = replacer(data)

				if LOG_FLAG == True:
					logging(logData, OUTGOING)

				dstSocket.sendall(data)


if __name__ == "__main__":
	# Parse arguments
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
		elif sys.argv[1].startswith("-auto"):
			LOG_FLAG = True
			AUTONUM = int(sys.argv[1][5:])
			LOG_COMMAND = "-autoN"
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
		elif sys.argv[1].startswith("-auto"):
			LOG_FLAG = True
			AUTONUM = int(sys.argv[1][5:])
			LOG_COMMAND = "-autoN"

	HOST = "localhost"
	DST_PORT = int(sys.argv[len(sys.argv) - 1])
	SERVER = sys.argv[len(sys.argv) - 2]
	SRC_PORT = int(sys.argv[len(sys.argv) - 3])

	if '-replace' in sys.argv: # if -replace is an argument
		REPLACE_FLAG = True
		replaceIndex = sys.argv.index('-replace')
		ORIGINAL_T = sys.argv[replaceIndex + 1]
		REPLACE_T = sys.argv[replaceIndex + 2]
		if ORIGINAL_T == str(SRC_PORT) or REPLACE_T == str(SRC_PORT):
			print("\nIncorrect Usage of -replace  ")
			print("Usage: ./A3.py [logOptions] [replaceOptions] srcPort server dstPort")
			print("[logOptions] and [replaceOptions] are optional parameters")
			print("[replaceOptions] takes in 2 parameters\n")
			sys.exit(0)
	
	#print(ORIGINAL_T,REPLACE_T)

	print("Port logger running: srcPort=" + str(SRC_PORT) + " host=" + SERVER + " dstPort=" + str(DST_PORT))
	#print("Log command = " + LOG_COMMAND)

	# Create socket to accept clients
	sourceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sourceSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sourceSocket.bind((HOST, SRC_PORT))
	sourceSocket.listen(5)

	while 1:
		client, addr = sourceSocket.accept()
		# get local time
		timeNow = time.strftime("%a %b %d %H:%M:%S")
		print("New Connection: " + timeNow + ", from " + str(addr[0]))

		# Create  socket that will forward data
		dstSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dstSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Connect to destination server
		dstSocket.connect((SERVER, DST_PORT))

		# Start a thread that will handle data between the sockets
		threading.Thread(target=clientHandler, args=(client, dstSocket)).start()