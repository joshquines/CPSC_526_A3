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
REPLACE: Not Tested -------------------------------------------------------------------------------------------------------
"""
#Read response as a string, replace target string with replacement string
def replacer(data):
	response = data.replace(ORIGINAL_T, REPLACE_T)
	return response

"""
LOGGING: Work in Progress ------------------------------------------------------------------------------------------------
"""
def logging(data, prefix):
	
	
	#RAW
	if LOG_COMMAND == "-raw":
		data = data.split(b'\n')
		#print("DEBUG: raw log")
		for line in data:
			line = line.decode("utf-8")
			print(prefix + " " +  str(line))




	#STRIP
	elif LOG_COMMAND == "-strip":
		data = data.split(b'\n')
		#print("DEBUG: strip log")
		for line in data:
			line= line.decode("utf-8")
			lineString = str(line)
			#print(prefix, end="")
			for x in lineString:
				#ADD CHECK IF PRINTABLE CHR HERE
				if not(x in string.printable):
					lineString = lineString.replace(x, ".")
				#print(str(x), end="")
			
			print(prefix + " " + lineString)


	#HEXDUMP
	elif LOG_COMMAND == "-hex":
		data = data.split(b'\n')
		#print("DEBUG: hex log")
		for line in data:
			line = line.decode("utf-8")
			lineString = str(line)
			#print(prefix, end="")
			for x in lineString:
				hx = ":".join("{:02x}".format(ord(c)) for c in x)
				lineString = lineString.replace(x,hx)
				#print(x, end="")
			print(prefix + " " + lineString)


	#AUTON
	elif LOG_COMMAND == "-autoN":
		print("DEBUG: autoN log")
		chunks = [data[i:i + n] for i in range(0, len(data), AUTONUM)]
		for x in chunks:
			xString = str(x)
			#print(prefix, end="")
			for y in x:
				y = str(y)
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
			#print("\n")
			print(prefix + xString)
		



def connection_handler(client, destination_socket):
	inputs = [client, destination_socket]

	while 1:
		readable, writeable, exceptional = select.select(inputs, [], [])
		for sock in readable:
	
			data = sock.recv(1024)
			modified_data = data

			# If no data provided, we close the current connection stream.
			if not data:
				print("No data provided. Connection closed.")
				client.close()
				destination_socket.close()
				return

			# Check if socket sending data is destination socket and if so, send data to the client
			if sock == destination_socket:

				if REPLACE_FLAG == True:
					modified_data = replacer(data)

				if LOG_FLAG == True:
					logging(data, INCOMING)
				"""
				if replace_option != "":

					modified_data = replace_data(option_one, option_two, data)

					# Encode it back
					modified_data = modified_data.encode()

				if log_option != "":

					message = log_data(log_option, modified_data, n_bytes)

					counter = 0
					while counter < len(message):

						print("<--- " + str(message[counter]) + "\n")

						counter += 1
				"""
				client.sendall(data)

			# Otherwise send data from client to the destination
			else:
				if REPLACE_FLAG == True:
					modified_data = replacer(data)

				if LOG_FLAG == True:
					logging(data, OUTGOING)
				"""
				if replace_option != "":

					modified_data = replace_data(option_one, option_two, data)

					# Encode it back
					modified_data = modified_data.encode()

				if log_option != "":

					message = log_data(log_option, modified_data, n_bytes)

					# Send the source message host to the destination
					counter = 0
					while counter < len(message):

						print("---> " + str(message[counter]) + "\n")

						counter += 1
				"""
				destination_socket.sendall(data)

"""
THIS IS STILL A2 CODE
"""
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
			#print("Log command = " + LOG_COMMAND)
		elif sys.argv[1].startswith("-auto"):
			LOG_FLAG = True
			AUTONUM = sys.argv[1][5:]
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
			print("Log command = " + LOG_COMMAND)
		elif sys.argv[1].startswith("-auto"):
			LOG_FLAG = True
			AUTONUM = sys.argv[1][5:]
			LOG_COMMAND = "-autoN"

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

	print("Port logger running: srcPort=" + str(SRC_PORT) + " host=" + SERVER + " dstPort=" + str(DST_PORT))
	#print("Log command = " + LOG_COMMAND)

	sourceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sourceSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#sourceSocket.setblocking(0)
	sourceSocket.bind((HOST, SRC_PORT))
	sourceSocket.listen(5)

	while 1:
		client, addr = sourceSocket.accept()
		

		timeNow = time.strftime("%a %b %d %H:%M:%S")
		print("New Connection: " + timeNow + ", from " + str(addr[0]))

		# Create a forwading socket that will forward information
		# obtained from the client to the destination through our server
		destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		destination_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#destination_socket.setblocking(0)
		# Connect to our destination server
		destination_socket.connect((SERVER, DST_PORT))

		# Start a thread that will handle the transfer of data between source and destination
		threading.Thread(target=connection_handler, args=(client, destination_socket)).start()