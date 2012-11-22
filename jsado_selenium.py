#!/usr/bin/python

# JS Auto DeObfuscator with Selenium by Luciano Giuseppe
# Useful on deobfuscation by a function as eval
#
#Dependencies: Selenium for python: http://pypi.python.org/pypi/selenium, Selenium server:http://seleniumhq.org/download/
#More infos: http://pypi.python.org/pypi/selenium

import subprocess
import sys
import os
import string
import random
from jsado import jsado

#for selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



# Main
if __name__ == "__main__":
	print("JS Auto DeObfuscator with Selenium\n")	

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
		
		#try to run the browser with the decrypter webpage
		print("Work completed: %s running..."%hack.browserName)
		if hack.browserName == "chrome":
			browser = webdriver.chrome.webdriver.WebDriver(executable_path='chromium-browser', port=9515);

		else:
			browser = webdriver.Firefox() # Get local session of firefox
	
		browser.get(hack.outputUrlName) # Load page
		print("If there're some ReferenceError errors in js console or the js deobuscated shows strange strings or seems to be obfuscated use increment!")
	
		#User want to increment the times that eval is normally executed
		answer = raw_input("\nDo you want to increment the n_execution? y/n : ")
		while (answer == "y"):
			execLimit += 1
			if (hack.applyHack(sys.argv[1], sys.argv[2], execLimit) == 0):
				print("An error occurred: byee!")
				sys.exit()
			print("Limit:%d - Page refreshing...\n"%execLimit)
			browser.refresh()
			answer = raw_input("Do you want to increment the n_execution? y/n : ")
	except WebDriverException as e:
		print("Selenium error: %s\n"%e.msg.strip())
		sys.exit(1)
	except Exception as e:
		print("Error: %s\n"%e)
		sys.exit(1)
	
	#exit
	print("Bye bye!!")
	
