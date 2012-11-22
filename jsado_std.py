#!/usr/bin/python

# JS Auto DeObfuscator Standard by Luciano Giuseppe
# Useful on deobfuscation by a function as eval

import subprocess
import sys
import os
import string
import random
from jsado import jsado

# Main
if __name__ == "__main__":
	print("JS Auto DeObfuscator Standard\n")	

	#checks the args
	argLen = len(sys.argv)	
	execLimit = 0
	if (argLen < 3):
		print( os.path.basename(__file__)+" file.html function_to_hack [n_execution]")
		sys.exit()
	elif(argLen == 4):
		try:	
			execLimit = int(sys.argv[3])
		except ValueError:
	    		print("Bad n_execution value: assume it as 0")
	
	try:	
		hack = jsado()
		#apply the hack to webpage 
		if(hack.applyHack(sys.argv[1], sys.argv[2], execLimit) == 0):
			print("An error occurred: byee!")
			sys.exit()
	
		#run the browser with the decrypter webpage
		print("Work completed: %s running..."%hack.browserName)
		subprocess.CREATE_NEW_CONSOLE=True
		subprocess.Popen([hack.browserName, hack.outputFileName]);
		print("If there're some ReferenceError errors in js console or the js deobuscated shows strange strings or seems to be obfuscated use increment!")
	
		#User want to increment the times that eval is normally executed
		answer = raw_input("\nDo you want to increment the n_execution? y/n : ")
		while (answer == "y"):
			execLimit += 1
			if (hack.applyHack(sys.argv[1], sys.argv[2], execLimit) == 0):
				print("An error occurred: byee!")
				sys.exit()
			print("Limit:%d - Refresh the page into browser"%execLimit)
			answer = raw_input("\nDo you want to increment the n_execution? y/n : ")
	except Exception as e:
		print("Error: %s\n"%e)
		sys.exit(1)
	#exit
	print("Bye bye!!")
	
