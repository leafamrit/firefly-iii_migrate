// javascript:(function(){document.body.appendChild(document.createElement('script')).src='https://raw.githubusercontent.com/Arkeyve/firefly-iii_migrate/master/formfill.js';})();

let inputstr = prompt("input");
inputstr = inputstr.split("\t");

let category = "Misc.";
let description = "Misc.";
if(inputstr[2].indexOf("zepto") >= 0) { category = "Groceries"; description = "Zepto"; }
if(inputstr[2].indexOf("paytm") >= 0) { category = "Snacks"; description = "Paytm"; }
if(inputstr[2].indexOf("swiggy") >= 0) { category = "Food"; description = "Swiggy"; }
if(inputstr[2].indexOf("DELOITTE") >= 0) { category = "Income"; description = "Deloitte"; }
if(inputstr[2].indexOf("parvatkarmukesh") >= 0) { category = "Polo GT"; description = "Car Cleaning"; }
if(inputstr[2].indexOf("CHANDRASEK") >= 0) { category = "Samarth Garden C/305"; description = "Rent"; }
if(inputstr[2].indexOf("decathlon") >= 0) { category = "Shopping"; description = "Decathlon"; }

document.querySelector("input[name='date[]']").value = inputstr[0].split("/").reverse().join("-");
document.querySelector("input[name='description[]']").value = description;
document.querySelector("input[name='amount[]']").value = inputstr[3] !== "0.0" ? Number(inputstr[3]) : Number(inputstr[4]);

document.querySelector("input[name='category[]']").value = category;
document.querySelector("input[name='create_another']").checked ? undefined : document.querySelector("input[name='create_another']").click();

if ("createEvent" in document) {
    var evt = document.createEvent("HTMLEvents");
    evt.initEvent("change", false, true);
    document.querySelector("input[name='description[]']").dispatchEvent(evt);
    document.querySelector("input[name='amount[]']").dispatchEvent(evt);
}
else {
    document.querySelector("input[name='description[]']").fireEvent("onchange");
    document.querySelector("input[name='amount[]']").fireEvent("onchange");
}
