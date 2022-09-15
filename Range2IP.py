import sys,ipaddress
from ipaddress import ip_address
from termcolor import colored
def getrange(line):
	startip, endip = line.strip().split('-')
	end = endip
	startip = int(ip_address(startip).packed.hex(),16)
	endip = int(ip_address(endip).packed.hex(),16)
	for ip in range(startip,endip):
		print(colored(ip_address(ip).exploded,'green'))
	print(colored(end,'green'))	
print("Welcome to Range2IP")
if sys.argv[1] == "-f":
	with open(sys.argv[2]) as file: 
		for line in file: getrange(line)		
else: getrange(sys.argv[1])
