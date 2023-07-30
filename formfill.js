function getJSON() {
  // javascript:(function(){document.body.appendChild(document.createElement('script')).src='https://raw.githubusercontent.com/Arkeyve/firefly-iii_migrate/master/formfill.js';})();

  const api_url = "http://<firefly-base-url>/api/v1/transactions";
  const auth_token = "<auth_token>";

  let inputstrArr = prompt("input");
  // inputstrArr = inputstrArr.split("\r\n"); // windows
  inputstrArr = inputstrArr.split("\n"); // linux

  inputstrArr.forEach((inputstr) => {
    inputstr = inputstr.split("\t");

    let category = "Misc.";
    let description = "Misc.";
    if (
      inputstr[2].search(/zepto/i) >= 0 ||
      inputstr[2].search(/dunzo/i) >= 0
    ) {
      category = "Groceries";
      description = "Zepto";
    }
    if (inputstr[2].search(/paytm/i) >= 0) {
      category = "Snacks";
      description = "Paytm";
    }
    if (inputstr[2].search(/swiggy/i) >= 0) {
      category = "Food";
      description = "Swiggy";
    }
    if (inputstr[2].search(/DELOITTE/i) >= 0) {
      category = "Income";
      description = "Deloitte";
    }
    if (inputstr[2].search(/parvatkarmukesh/i) >= 0) {
      category = "Polo GT";
      description = "Car Cleaning";
    }
    if (inputstr[2].search(/CHANDRASEK/i) >= 0) {
      category = "Samarth Garden C/305";
      description = "Rent";
    }
    if (inputstr[2].search(/decathlon/i) >= 0) {
      category = "Shopping";
      description = "Decathlon";
    }
    if (inputstr[2].search(/tpslqr/i) >= 0) {
      category = "Samarth Garden C/305";
      description = "Electricity";
    }
    if (inputstr[2].search(/akshayamrit/i) >= 0) {
      category = "Lending/Owing";
      description = "Ishu Bhaiya";
    }
    if (inputstr[2].search(/atkare/i) >= 0) {
      category = "Lending/Owing";
      description = "Akash Atkare";
    }
    if (inputstr[2].search(/nehakalani/i) >= 0) {
      category = "Lending/Owing";
      description = "Neha";
    }
    if (inputstr[2].search(/uber/i) >= 0) {
      category = "Commute";
      description = "Uber";
    }
    if (inputstr[2].search(/airtelprepaidMu/i) >= 0) {
      category = "Phone";
      description = "Airtel";
    }

    let date = inputstr[0].split("/").reverse().join("-");
    let amount = inputstr[3].trim();
    let amountDep = inputstr[4].trim();

    let transType = Number(amount) > 0 ? "withdrawal" : "deposit";

    let requestObj = {
      error_if_duplicate_hash: false,
      apply_rules: true,
      transactions: [
        {
          type: transType,
          date: `${date}T00:00:00`,
          amount: Number(amount) > 0 ? amount : amountDep,
          description: description,
          category_name: category,
          source_name: Number(amount) > 0 ? "ICICI Anishabad" : null,
          destination_name: Number(amountDep) > 0 ? "ICICI Anishabad" : null,
        },
      ],
    };

    // POST REQUEST
    var data = JSON.stringify(requestObj);
    
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    
    xhr.addEventListener("readystatechange", function() {
      if(this.readyState === 4) {
        console.log(this.responseText);
      }
    });
    
    xhr.open("POST", api_url);
    xhr.setRequestHeader("Authorization", auth_token);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.send(data);

    console.log(JSON.stringify(requestObj));
    // navigator.clipboard.writeText(JSON.stringify(requestObj));
  });
}
