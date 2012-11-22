JS Auto DeObfuscator 
========================

##About
JSADO automatically deobfuscate javascript scripts which use eval or some other function, one or more time, to de-obfuscat it-self.
This tool hopes to be useful to security researches for speed up their work.
It uses to work as default browser Firefox, but at last line of the source you can change firefox with an other browser as Chrome, obviously.

#Dependencies
jsado_selenium.py to run has need of: 
* Selenium for python: http://pypi.python.org/pypi/selenium
* Selenium server:http://seleniumhq.org/download/
* ChromeDriver for Chrome support: https://code.google.com/p/chromedriver/

##How to use
If you want to use jsado_selenium.py, you need to run the selenium-server: java -jar selenium-server-standalone-2.25.0.jar
If you want to use Chrome with jsado_selenium.py, you must to run only the ChromeDriver.

After that you can use these scripts:

python jsado.py file.html function_to_hack [n_execution=0] 

python jsado_selenium.py file.html function_to_hack [n_execution=0] 

For example: you can call this script with: "python jsado.py obf.html eval" to don't let's execute eval in obf.html and get into the browser all js code executed with eval.
You can use the increment to let execute eval one time, for example: the first time with eval there are some variables declaration.

##How JSADO works
JSADO injects into the webpage a js script, that hook the function. Once the function hooked is executed, the js script injected shows a pannel with the code catched.

##Personalization
You can open jsado.py and edit: browserName, outputFileName or decomment in hackStr the import of js beautify
For jsado_selenium.py and Chrome: the default port is 9515, if you need: change it.

##Developer
[Luciano Giuseppe] (http://sites.google.com/site/lucianogiuseppeprogrammi/)
