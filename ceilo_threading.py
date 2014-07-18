import subprocess 
import re
import sys

var = raw_input("Please enter the number of times you want to run the test: ")

for i in range(0, int(var)):
    p = subprocess.Popen('python ceilo_run_commands.py', shell=True)
    p.wait() 

subprocess.call(['./flush-alarms.sh'])

