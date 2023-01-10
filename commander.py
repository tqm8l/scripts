#v1 Tom
import sys
import os
command = sys.argv[1]
file = sys.argv[2]
with open(file, 'r') as file:
    for line in file:
        os.system(command + ' ' + line)
