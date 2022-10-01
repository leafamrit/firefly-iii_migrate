let inputstr = prompt("input");
inputstr = inputstr.split("\t");

document.querySelector("input[name='date[]']").value = inputstr[0].split("/").reverse().join("-");
document.querySelector("input[name='description[]']").value = inputstr[2];
document.querySelector("input[name='amount[]']").value = inputstr[3] !== "0.0" ? inputstr[3] : inputstr[4];

let category = "Misc.";
if(inputstr[2].indexOf("zepto") >= 0) category = "Groceries";
if(inputstr[2].indexOf("paytm") >= 0) category = "Snacks";
if(inputstr[2].indexOf("swiggy") >= 0) category = "Food";
if(inputstr[2].indexOf("DELOITTE") >= 0) category = "Income";
if(inputstr[2].indexOf("parvatkarmukesh") >= 0) category = "Polo GT";
if(inputstr[2].indexOf("CHANDRASEK") >= 0) category = "Samarth Garden C/305";
if(inputstr[2].indexOf("decathlon") >= 0) category = "Shopping";

document.querySelector("input[name='category[]']").value = category;
document.querySelector("input[name='create_another']").checked = true;
