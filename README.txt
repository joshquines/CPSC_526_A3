CPSC 526 Assignment #3

Steven Leong 10129668 T01
Josh Quines 10138118 T03


How to run: python3 proxy.py [logOptions] [replaceOptions] srcPort server destPort

Options Usage
[logOptions]:	  -raw, -strip, -hex, -auto<N> where N is an int
[replaceOptions]: -replace <target> <targetReplacement>	 

How to connect:
	
	Client: nc localhost <srcPort>
	Server: nc localhost <destPort>

Supported Logging Options:
	-raw: 	Raw output
	-strip:	Replace unprintable characters with "."
	-hex:	Hexdump
	-autoN:	Output in N-sized chunks

