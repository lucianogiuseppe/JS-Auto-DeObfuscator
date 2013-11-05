#!/usr/bin/python

# JS Auto DeObfuscator 0.7.2 by Luciano Giuseppe
# Useful on eval deobfuscation code
#
#Dependencies: Selenium for python: http://pypi.python.org/pypi/selenium, Selenium server:http://seleniumhq.org/download/
#More infos: http://pypi.python.org/pypi/selenium

import subprocess
import sys
import os
import string
import random


##You can personalize these params!!
useSelenium = False # True o False
browserName = "firefox" #the command to run your browser or the complete path
outputFileName = "t.html" #output filename
##End of pesonalization params!!


#check selenium presence
canUseSelenium = True
try:
	from selenium import webdriver
	from selenium.common.exceptions import NoSuchElementException, WebDriverException
	from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
except:
	canUseSelenium = False


#JS Auto DeObfuscator Class by Luciano Giuseppe
class jsado:
	
	#Init some class attributes
	#browserName: the commandline istruction to run your browser
	#outputFileName: output filename
	def __init__(self, browserName, outputFileName, injS = False):
		self.fileTxt = None;
		self.browserName = browserName
		self.outputFileName = os.getcwd() + os.sep + outputFileName
		self.outputUrlName = "file://"+self.outputFileName
		self.injectStart = injS

	#return a random string 
	def __r(self):
		size = random.randint(4, 12)
		return ''.join(random.choice(string.ascii_letters) for x in xrange(size))

	#get the js code to inject into page
	def __getHackString(self,f, l):
		hackStr = string.Template("""
		<script type="text/javascript">
		(function () {
		var $memFct = $function;
		$cont = 0;
		$str = "";
		$beautify = function(text) {
			if(window.js_beautify)
				text = js_beautify(text)
			return text.replace(/[<>"&]/g, function(s) {return '&#' + s.charCodeAt(0) + ';'; });
		};
		$function = function(code) {

			//parse the input
			var input;
			if(typeof(code) === "object") {
				var str = "Object Dump:<br/>";
				for(var t in input) {
					str += t +":"+code[t]+"<br/>";			
				}
				input = str;			
			} else if(typeof(code) === "string") {
				input = $beautify(code)
			}
			
			//get in output
			$cont++;
			if(window.$code == undefined || window.$code.$cont == undefined)$str += $cont + ")" + input +"<br/><br/>";
			
			if($cont == 1) {
				//create the output view
				var $div = document.createElement("div");
				$div.setAttribute("style", "width:95%; height:95%; overflow:no;z-index:100;position:fixed;bottom:0;left:0;border:1px solid black; background:#cccccc;");
				var button = document.createElement("button");
				button.innerHTML = "Minimize";
				button.addEventListener("click", function() {
					var $p = this.parentNode;				
					if($p.style.height=="30px") {
						$p.childNodes[1].style.display="block";
						$p.style.height="95%";
						this.innerHTML="Minimize";
					} else {
						$p.childNodes[1].style.display="none";
						$p.style.height="30px";
						this.innerHTML="Maximize";
					}
				});
				$div.appendChild(button);
				$code = document.createElement("pre");
				$code.setAttribute("readonly", "readonly");
				$code.setAttribute("style","display:block; height:94%; width:96%; overflow-y:scroll;color:black;border: 1px solid #AAAAAA;background:white;font-size:14px;margin:0 0 0 3px;word-break:break-word;word-break:break-all;white-space:pre-wrap;");
				$div.appendChild($code);
				//document object exists?
				if(document.body === undefined || document.body === null)	{		
					addEventListener("DOMContentLoaded", function() {
						$code.innerHTML = $str;
						document.body.appendChild($div);
						$code.$cont = true; //say that I'm in dom
					});
				} else {
					$code.innerHTML = $str;
					document.body.appendChild($div);
					$code.$cont = true; //say that I'm in dom
				}
				
			} else {
				if(document.body !== undefined || document.body !== null) {
					$code.innerHTML += $cont+ ")<br/>"+ input + "<br/><br/>";
				}
			}
	
			if($cont <= $limit) { //can it exec $function
				return $memFct(code); 
			}
		};
		})()</script>\n""");
		return hackStr.substitute({'function': f, 'limit' : l, 'memFct' : self.__r(), 'cont': self.__r(), 'str' : self.__r(), 'div': self.__r(), 'code': self.__r(), 'oldOnError' : self.__r(), 'p' : self.__r(), 'beautify' : self.__r()})

	#apply the hack to webpage for deobfuscate the js code
	def applyHack(self, fileInput, functionName, limitExecution, useJB):
		try:
			if self.fileTxt is None: #only the first time
				with open(fileInput, 'r') as f:
					self.fileTxt = f.read()
					

			#generate the js code to inject into html
			injString = ""	
			if useJB == True:
				injString += "<script src=\"beautify.js\" type=\"text/javascript\"></script>" #you should download js lib from https://github.com/einars/js-beautify
			injString += self.__getHackString(functionName, limitExecution)
			
			#inject into html page
			outHtml = self.fileTxt
			if self.injectStart == True:
				outHtml = injString + outHtml
			else:
				if outHtml.find("<head>") != -1:
					injString = "<head>"+injString
					outHtml = outHtml.replace("<head>", injString)
				elif outHtml.find("<html>") != -1:
					injString = "<html><head>"+injString+"</head>"
					outHtml = outHtml.replace("<html>", injString)
				else:
					self.injectStart = True #for the next iteration
					outHtml = injString + outHtml
			
			#write the output html file
			with open(self.outputFileName, 'w') as outFile:
				outFile.write(outHtml)

		except IOError as e:
			print("I/O error({0}): {1}".format(e.errno, e.strerror))
			return 0
		else:
			return 1


#Browser launcher factory
class LauncherFactory(object):
	def __new__(cls, selenium):
		if selenium == True:
			return LauncherSelenium()
		else:
			return LauncherNormal()

#Launcher that use Selenium to inteface with browser
class LauncherSelenium:
	browser = None

	def start(self,browserName, outputUrlName):
		if browserName == "chrome":
			self.browser = webdriver.chrome.webdriver.WebDriver(executable_path='chromium-browser', port=9515);
		else:
			self.browser = webdriver.Firefox() # Get local session of firefox
		self.browser.get(outputUrlName) # Load page
	
	def refresh(self):
		if self.browser == None:
			return
		print("Page refreshing...\n")
		self.browser.refresh()

#Normal browser launcher
class LauncherNormal:

	def start(self, browserName, outputUrlName):
		subprocess.CREATE_NEW_CONSOLE=True
		subprocess.Popen([hack.browserName, hack.outputFileName]);
	
	def refresh(self):
		print("You should refresh page into browser\n")
		return



#Parse the argv
def parseArgv(argv):
	global useSelenium, canUseSelenium
	execLimit = 0
	useJsBeauty = False
	injStart = False
	
	argLen = len(sys.argv)
	for x in xrange(3,argLen): 
		str = argv[x].split(':')
		matchStr = str[0].lower()
		if matchStr == "nexec":
			try:	
				execLimit = int(str[1])
			except ValueError:
		    		print("Bad nExec value: assume it as 0")
		elif matchStr == "usejb":
			useJsBeauty = True;
		elif matchStr == "uses" and canUseSelenium == True:
			useSelenium = True
		elif matchStr == "injstart": 
			injStart = True
	
	return [execLimit, useJsBeauty, injStart]

# Main
if __name__ == "__main__":
	print("JS Auto DeObfuscator\n")	

	#checks the args
	execLimit = 0
	useJsBeauty = False
	injStart = False

	argLen = len(sys.argv)	
	if (argLen < 3):
		print("How to use:\n"+ os.path.basename(__file__)+" file.html function_to_hack [nExec:number] [useJB] [useS] [injStart]\n\nSee the site for more information:\nhttp://github.com/lucianogiuseppe/JS-Auto-DeObfuscator")
		sys.exit()
	else:
		execLimit, useJsBeauty, injStart = parseArgv(sys.argv);
	
	try:	
		#Prepare the jsado
		hack = jsado(browserName, outputFileName, injStart)
		#Prepare the browser launcher
		launcher = LauncherFactory(useSelenium)

		#apply the hack to webpage
		if(hack.applyHack(sys.argv[1], sys.argv[2], execLimit, useJsBeauty) == 0):
			print("An error occurred: byee!")
			sys.exit()
		
		#try to run the browser with the decrypter webpage
		print("Work completed: %s running..."%hack.browserName)
		launcher.start(hack.browserName, hack.outputUrlName)

		#Some descryption about the use
		print("If there're some ReferenceError errors in js console or the js deobuscated shows strange strings or seems to be obfuscated use 'increment'!\n")
	
		#User want to increment the times that eval is normally executed
		question = "Do you want to increment the %s execution times? yes/no : "%sys.argv[2]
		answer = raw_input(question)
		while answer.lower() in ('y', 'yes'):
			execLimit += 1
			if (hack.applyHack(sys.argv[1], sys.argv[2], execLimit, useJsBeauty) == 0):
				print("An error occurred: byee!")
				sys.exit()
			print("%s execution limit:%d"%(sys.argv[2],execLimit))
			launcher.refresh() #refresh the page
			answer = raw_input(question)
	except Exception as e:
		print("Error: %s\n"%e)
		sys.exit(1)
	
	#exit
	print("Bye bye!!")
	
