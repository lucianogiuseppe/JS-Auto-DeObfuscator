JS Auto DeObfuscator 
========================

##About
JsADO automatically deobfuscate javascript scripts which use eval or some other function, one or more time, to de-obfuscat it-self.
This tool hopes to be useful to security researches for speed up their work.
It uses to work as default browser Firefox, but at last line of the source you can change firefox with an other browser as Chrome, obviously.

#Dependencies
JsADO with Selenium needs to run: 
* Selenium for python: http://pypi.python.org/pypi/selenium
* Selenium server:http://seleniumhq.org/download/
* ChromeDriver for Chrome support: https://code.google.com/p/chromedriver/

##How to use
If you want to use Firefox with Selenium you must run the selenium-server: java -jar selenium-server-standalone-XX.jar
If you want to use Chrome with Selenium you must run only the ChromeDriver.

After that you can use these scripts: download jsado.py and run

python jsado.py file.html function_to_hack [nExec:0] [useJB] [useS]

where 
	nExec says that the function_to_hack have to be executed nExec times normally
	useJB says to use "js beautify" to show the output
	useS says to use Selenium

For example: you can call this script with: "python jsado.py obf.html eval" to don't let's execute eval in obf.html and get into the browser all params passed to eval.
You can use the increment to let execute eval one time, for example: the first time with eval there are some variables declaration.

##How JsADO works
JsADO injects into the webpage a js script, that hook the function. Once the function hooked is executed, the js script injected shows a pannel with the code catched.

##Personalization
You can open jsado.py and change: browserName, outputFileName and useSelenium to don't set 'useS' every time.
For Selenium and Chrome: the default port is 9515, if you need: change it.

##Developer
[Luciano Giuseppe] (http://sites.google.com/site/lucianogiuseppeprogrammi/)
