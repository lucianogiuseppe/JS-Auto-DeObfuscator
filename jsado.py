#!/usr/bin/python

# JS Auto DeObfuscator v. 0.5.3 by Luciano Giuseppe
# Useful on deobfuscation by a function as eval

import subprocess
import sys
import os
import string
import random

#JS Auto DeObfuscator
class jsado:
	#you can personalize these:
	browser = "firefox" #the commandline istruction to run your browser
	outputFileName = "t.html"
	
	def __init__(self):
		self.fileTxt = None;

	#return a random string 
	def __r(self):
		size = random.randint(4, 12)
		return ''.join(random.choice(string.ascii_letters) for x in xrange(size))

	#get the js code to inject into page
	def __getHackString(self,f, l):
		hackStr = string.Template("""<script src="http://jsbeautifier.org/beautify.js" type="application/javascript"></script>
		<script type="application/javascript">
		(function () {
		var $memFct = $function;
		$cont = 0;
		$str = "";
		$function = function(ttt) {
			if(typeof(ttt) === "object") {
				var str = "Object Dump:\\n\\n";
				for(var t in ttt) {
					str += t +":"+ttt[t]+"\\n";			
				}
				ttt = str;			
			}
			$cont++;		
			$str += $cont+ ")" +ttt +"\\n\\n";
			if($cont == 1) {
				var $div = document.createElement("div");
				$div.setAttribute("style", "width:95%; height:95%; overflow:no;z-index:100;position:absolute;bottom:0;left:0;border:1px solid black; background:white;");
				var $button = document.createElement("button");
				$button.innerHTML = "Minimize";
				$button.addEventListener("click", function() {
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
				$div.appendChild($button);
				$code = document.createElement("textarea");
				$code.setAttribute("readonly", "readonly");
				$code.setAttribute("style","display:block; height:95%; width:98%; overflow:auto");
				$div.appendChild($code);
				if(document.body === undefined || document.body === null)	{		
					addEventListener("load", function() {
						$code.innerHTML = js_beautify($str);
						document.body.appendChild($div);
					});
				} else {
					$code.innerHTML = js_beautify($str);
					document.body.appendChild($div);
				}
	
			} else
				if(document.body !== undefined || document.body !== null)	
					$code.innerHTML += "\\n\\n"+ js_beautify($cont+ ")" +ttt +"\\n\\n");

			if($cont <= $limit) { return $memFct(ttt); }

		};
		})()</script>\n""");
		return hackStr.substitute({'function': f, 'limit' : l, 'memFct' : self.__r(), 'cont': self.__r(), 'str' : self.__r(), 'div': self.__r(), 'code': self.__r(), 'oldOnError' : self.__r(), 'button' : self.__r(), 'p' : self.__r()})

	#apply the hack to webpage for de-obfuscate the js code
	def applyHack(self, fileInput, functionName, limitExecution):
		try:
			if self.fileTxt is None:
				with open(fileInput, 'r') as f:
					self.fileTxt = f.read()

			with open(self.outputFileName, 'w') as outFile:
				outFile.write(self.__getHackString(functionName, limitExecution)+self.fileTxt)

		except IOError as e:
			print("I/O error({0}): {1}".format(e.errno, e.strerror))
			return 0
		else:
			return 1

# Main
if __name__ == "__main__":
	print("JS Auto DeObfuscator v. 0.5.1\n")	

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
		print("Work completed: %s running..."%hack.browser)
		subprocess.CREATE_NEW_CONSOLE=True
		subprocess.Popen([hack.browser, hack.outputFileName]);
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
	
