window.onload = function() {
  dayearlier.addEventListener("click", () => { newdate("day", "minus") });
  daylater.addEventListener("click", () => { newdate("day", "plus") });
}

function newdate(period, plusminus) {
  
  currentdate = new Date();
  
  var Longdt = document.getElementById("longDate");
  var ISOdt = document.getElementById("dateISO");
  
  if (period=="day" || period=="week") {
    
    if (period=="day") {
      milliseconds = 60*60*24*1000; // one day in milliseconds

    }
    if (period=="week") {
      milliseconds = 7*60*60*24*1000; // one week in milliseconds
    }
    
    currentdate = Date.parse(ISOdt.value);
    
    
    if (plusminus=="minus") {
      var newdate = new Date(currentdate.valueOf() - milliseconds); 
    }
    else {
      var newdate = new Date(currentdate.valueOf() + milliseconds); 
    }
    Longdt.innerText=newdate.toDateString();
    ISOdt.value=newdate.toISOString();
  }
}