import sys
import os
import string
import random

#JS Auto DeObfuscator Class v .6 by Luciano Giuseppe
class jsado:
	#you can personalize these:
	browserName = "firefox" #the commandline istruction to run your browser
	outputFileName = "t.html"
	
	def __init__(self):
		self.fileTxt = None;
		self.outputFileName = os.getcwd() + os.sep + self.outputFileName
		self.outputUrlName = "file://"+self.outputFileName

	#return a random string 
	def __r(self):
		size = random.randint(4, 12)
		return ''.join(random.choice(string.ascii_letters) for x in xrange(size))

	#get the js code to inject into page
	def __getHackString(self,f, l):
		hackStr = string.Template("""<!-- Decomment to use jsBeautify <script src="http://jsbeautifier.org/beautify.js" type="application/javascript"></script>-->
		<script type="application/javascript">
		(function () {
		var $memFct = $function;
		$cont = 0;
		$str = "";
		$beautify = function(text) {
			if(window.js_beautify)
				text = js_beautify(text)
			return text.replace("&","&amp;",'g').replace("<","&lt;",'g').replace(">","&gt;",'g');
		};
		$function = function(input) {
			//parse the input
			if(typeof(input) === "object") {
				var str = "Object Dump:<br/>";
				for(var t in input) {
					str += t +":"+input[t]+"<br/>";			
				}
				input = str;			
			} else if(typeof(input) === "string") {
				input = $beautify(input)
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
				$code.setAttribute("style","display:block; height:94%; width:96%; overflow:scroll;color:black;border: 1px solid #AAAAAA;background:white;font-size:14px;margin:0 0 0 3px;");
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
	
			if($cont <= $limit) { return $memFct(input); }
		};
		})()</script>\n""");
		return hackStr.substitute({'function': f, 'limit' : l, 'memFct' : self.__r(), 'cont': self.__r(), 'str' : self.__r(), 'div': self.__r(), 'code': self.__r(), 'oldOnError' : self.__r(), 'p' : self.__r(), 'beautify' : self.__r()})

	#apply the hack to webpage for deobfuscate the js code
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
