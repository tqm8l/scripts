import sys
import ipaddress
from termcolor import colored
print("Welcome to CIDR2IP")

try:
	cidr = str(sys.argv[1])
	for ip in ipaddress.IPv4Network(cidr):
		newip = str(ip)
		print(colored(newip,'green'))
except Exception as e:
	print(colored("broke",'red'))
