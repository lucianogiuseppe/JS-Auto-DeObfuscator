#!/usr/bin/python

# JS Auto DeObfuscator v. 0.5 by Luciano Giuseppe
# Useful on deobfuscation by a function as eval

import subprocess
import sys
import os
import string
import random

outputFileName = "t.html"

def r():
	size = random.randint(4, 12)
	return ''.join(random.choice(string.ascii_letters) for x in xrange(size))

def getHackString(f, l):
	hackStr = string.Template("""<script src="http://jsbeautifier.org/beautify.js" type="application/javascript"></script>
	<script type="application/javascript">
	(function () {
	var $memFct = $function;
	$cont = 0;
	$str = "";
	$function = function(ttt) {
		$cont++;		
		$str += $cont+ ")" +ttt +"\\n\\n";
		if($cont == 1) {
			var $div = document.createElement("div");
			$div.setAttribute("style", "width:95%; height:95%; overflow:no;z-index:100;position:absolute;bottom:0;left:0;border:1px solid black; background:white;");
			var $button = document.createElement("button");
			$button.innerHTML = "Open/Close";
			$button.addEventListener("click", function() {
				var $p = this.parentNode;				
				if($p.style.height=="30px") {
					$p.childNodes[1].style.display="block";
					$p.style.height="95%";
				} else {
					$p.childNodes[1].style.display="none";
					$p.style.height="30px";
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
	return hackStr.substitute({'function': f, 'limit' : l, 'memFct' : r(), 'cont': r(), 'str' : r(), 'div': r(), 'code': r(), 'oldOnError' : r(), 'button' : r(), 'p' : r()})

def applyHack(fileInput, function, limitExecution):
	try:
		f = open(fileInput, 'r');
		fileTxt = f.read()
		f.close()
		outFile = open(outputFileName, 'w')
		outFile.write(getHackString(function, limitExecution)+fileTxt)
		outFile.close()
	except IOError as e:
		print("I/O error({0}): {1}".format(e.errno, e.strerror))
		return 0
	else:
		return 1

# Main
if __name__ == "__main__":
	print("JS Auto DeObfuscator v. 0.5\n")	

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
	 
	if(applyHack(sys.argv[1], sys.argv[2], execLimit) == 0):
		print("An error occurred: byee!")
		sys.exit()

	print("Work completed: browser running...")
	subprocess.CREATE_NEW_CONSOLE=True
	subprocess.Popen(["firefox", outputFileName]);
	print("If there're in some ReferenceError errors in js console or the js deobuscated shows strange strings or seems to be obfuscated use increment!")
	
	answer = raw_input("\nDo you want to increment the n_execution? y/n : ")
	while (answer == "y"):
		execLimit += 1
		if (applyHack(sys.argv[1], sys.argv[2], execLimit) == 0):
			print("An error occurred: byee!")
			sys.exit()
		print("Limit:%d - Refresh the page into browser"%execLimit)
		answer = raw_input("\nDo you want to increment the n_execution? y/n : ")
	
	print("Bye bye!!")
	
