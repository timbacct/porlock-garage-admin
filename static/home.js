function clearFilters(){
  document.getElementById("customername").value = "";
  document.getElementById("registrationnumber").value = "";
  document.getElementById("datein").value = "";
  document.getElementById("makemodel").value = "";
  document.getElementById("phonenumber").value = "";
  document.getElementById("period").value = "all";
  document.getElementById("estimates").value = "";
  document.getElementById("invoices").value = "invoices";
  
}
function showAlert(alertText){
  alert(alertText);
}

function toggleDateType(){
  var elem = document.getElementById("datetype");
  var elemval = document.getElementById("datetypevalue");
 
  if (elem.value=="In") {
    elem.value="Paid";
    elemval.value="Paid";
  } else {
    elem.value="In";
    elemval.value="In";
  }
  
}

window.onload = function() {
  var all = document.getElementById('all');
  var today = document.getElementById('today');
  var thisweek = document.getElementById('thisweek');
  var thismonth = document.getElementById('thismonth');
  var thisyear = document.getElementById('thisyear');

  all.onclick = allhandler;
  today.onclick = todayhandler;
  thisweek.onclick = thisweekhandler;
  thismonth.onclick = thismonthhandler;
  thisyear.onclick = thisyearhandler;

  dayearlier.addEventListener("click", () => { newdate("day", "minus") });
  daylater.addEventListener("click", () => { newdate("day", "plus") });
  weekearlier.addEventListener("click", () => { newdate("week", "minus") });
  weeklater.addEventListener("click", () => { newdate("week", "plus") });
  monthearlier.addEventListener("click", () => { newdate("month", "minus") });
  monthlater.addEventListener("click", () => { newdate("month", "plus") });
  yearearlier.addEventListener("click", () => { newdate("year", "minus") });
  yearlater.addEventListener("click", () => { newdate("year", "plus") });
  //alert("got here");
  //sumTableExVAT();
  //sumTableIncVAT();
}

function allhandler() {
  document.getElementById("start").value = "";
  document.getElementById("end").value = "";
  //alert('clicked');
}

function todayhandler() {
  const date = new Date().toLocaleDateString();
  let currentDate = '${day}-${month}-${year}';
  document.getElementById("start").value = date;
  document.getElementById("end").value = date;
  //alert('clicked');
}

function thisweekhandler() {
  const today = new Date();
  const firstDay = new Date(today.setDate(today.getDate() - today.getDay()));
  const lastDay = new Date(today.setDate(today.getDate() - today.getDay() + 6));
  document.getElementById("start").value = firstDay.toLocaleDateString();
  document.getElementById("end").value = lastDay.toLocaleDateString();
  //alert('clicked');
}

function thismonthhandler() {
  const now = new Date();
  const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
  const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
  document.getElementById("start").value = firstDay.toLocaleDateString();
  document.getElementById("end").value = lastDay.toLocaleDateString();
  //alert('clicked');
}

function thisyearhandler() {
  const currentYear = new Date().getFullYear();
  const firstDay = new Date(currentYear, 0, 1);
  const lastDay = new Date(currentYear, 11, 31);
  document.getElementById("start").value = firstDay.toLocaleDateString();
  document.getElementById("end").value = lastDay.toLocaleDateString();
  //alert('clicked');
}

function isoDate(datestr) {
  //alert(datestr);
  dateisostr = datestr.substring(6) + "-" + datestr.substring(3,5) + "-" + datestr.substring(0,2);
  //alert(date);
  return dateisostr;
}

function monthcalc(inputdate, plusminus) {
  // accepts date in string format dd/mm/yyyy
  //plusminus is plus to add a month and minus to subtract a month
  month = parseInt(inputdate.substring(3,5));
  if (plusminus=="minus") {
    month=month-1;
    if (month==0) {
      month = 12;
    }          
  }
  else {
    month=month+1;
    if (month==13) {
      month = 1;
    }
  }
  if (month < 9) {
    monthstr = "0" + month.toString();
  }
  else {
    monthstr = month.toString();
  }
  outputdate=inputdate.substring(0,2) + "/" + monthstr + "/"+ inputdate.substring(6);
  return outputdate;
}

function yearcalc(inputdate, plusminus) {
  // accepts date in string format dd/mm/yyyy
  //plusminus is plus to add a month and minus to subtract a month
  year = parseInt(inputdate.substring(6));
  if (plusminus=="minus") {
    year=year-1;
  }
  else {
    year=year+1;
  }
  outputdate=inputdate.substring(0,2) + "/" + inputdate.substring(3,5) + "/" + year;
  return outputdate;
}

function newdate(period, plusminus) {
  date = new Date();
  var start = document.getElementById("start");
  var end = document.getElementById("end");  
  if (period=="day" || period=="week") {
    if (period=="day") {
       milliseconds = 60*60*24*1000; // one day in milliseconds
    }
    if (period=="week") {
       milliseconds = 7*60*60*24*1000; // one week in milliseconds
    }

    startdate = Date.parse(isoDate(start.value));
    enddate = Date.parse(isoDate(end.value));
    if (plusminus=="minus") {
      var newstartdate = new Date(startdate.valueOf() - milliseconds); 
      var newenddate = new Date(enddate.valueOf() - milliseconds);
    }
    else {
      var newstartdate = new Date(startdate.valueOf() + milliseconds); 
      var newenddate = new Date(enddate.valueOf() + milliseconds);
    }
    start.value=newstartdate.toLocaleDateString();
    end.value=newenddate.toLocaleDateString();
  }
  
  if (period=="month")  {
    start.value = monthcalc(start.value, plusminus);
    end.value = monthcalc(end.value, plusminus);
  }
  if (period=="year")  {
    start.value = yearcalc(start.value, plusminus);
    end.value = yearcalc(end.value, plusminus);
  }

}
