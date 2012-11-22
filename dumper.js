/*
 * Arguments dumper by Luciano Giuseppe
 * It's just an example
 */
 
 /**
	How to use:
	If you see code like this: 
	window[tb('-57,-45,-46,-38,-55,-42,-40,-72,-45,-74,-85,-90')] = function(color) {
		return 'rgb(' + HexToR(color) + ',' + HexToG(color) + ',' + HexToB(color) + ')'
	
	You can use the dumper into function to get output:
	function tb(str) {
		dump("in", str);
		....//string decrypting code
		dump("out", rs);
		return rs
	}
	
	And you will get this into the webpage:
	1)
	-46,-58,-61,-40,-51,-47,-55,-41,-61,-54,-39,-46,-57,-40,-51,-45,-46,-61,-57,-59,-48,-48,-55,-56
	nb_times_function_called
*/


var cont = 0;  //I suggest you to rename it
var outputString = ""; //I suggest you to rename it

/* Dump params of a function
 * input = input value of the function to check
 * type : can be "in" or "out"
*/
function dump(type, input) {
	if(typeof(input) === "object") {
		var str = "Object:<br/>{";
		for(var t in input) {
			str += t +":"+input[t]+",";			
		}
		str = str.substring(0, str.length-1) + "}";
		input = str;			
	} else if(typeof(input) === "string") {
		input = input.replace("&","&amp;",'g').replace("<","&lt;",'g').replace(">","&gt;",'g');
	}
	if(window.outputCode === undefined || outputCode.inDom === undefined) {	
		outputString += formatString(type, input);
	}
	
	if(cont == 1 && !window.outputCode) {
		var div = document.createElement("div");
		div.setAttribute("style", "width:95%; height:95%; overflow:no;z-index:100;position:fixed;bottom:0;left:0;border:1px solid black; background:#cccccc;");
		var button = document.createElement("button");
		button.innerHTML = "Minimize";
		button.addEventListener("click", function() {
			var p = this.parentNode;				
			if(p.style.height=="30px") {
				p.childNodes[1].style.display="block";
				p.style.height="95%";
				this.innerHTML="Minimize";
			} else {
				p.childNodes[1].style.display="none";
				p.style.height="30px";
				this.innerHTML="Maximize";
			}
		});
		div.appendChild(button);
		outputCode = document.createElement("pre");
		outputCode.setAttribute("style","display:block; height:94%; width:96%; overflow:scroll;color:black;border:1px solid #AAAAAA;background:white;font-size:14px;margin:0 0 0 3px;");
		div.appendChild(outputCode);
		if(document.body === undefined || document.body === null)	{		
			addEventListener("load", function() {
				outputCode.innerHTML = outputString;
				document.body.appendChild(div);
				outputCode.inDom =true;
			});
		} else {
			outputCode.innerHTML = outputString;
			document.body.appendChild(div);
			outputCode.inDom =true;
		}

	} else
		if(document.body !== undefined || document.body !== null) {
			outputCode.innerHTML +=  formatString(type, input);
		}
}

function formatString(type, input) {
	var str = "";
	if(type == "in") {cont++; str += cont+ ")<br/>"; }
	str += input +"<br/>";
	if(type == "out") str += "<br/>";
	return str;
}