from flask import Flask, render_template, request, redirect, url_for, make_response
from logic import *
from buttonhandlers import *
from database import getInvoiceHeaders, getInvoiceHeader, getInvoiceHeadersTotal, getParts, getWork, getLastUpdate, getBookings, saveBookingToDB


app = Flask(__name__)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  print ("get here L1")
  if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'etcetera':
      error = 'Invalid Credentials.  Please try again.'
      return render_template('login.html', error=error)
    else:
      resp=make_response(f"The Cookie has been set")
      resp.set_cookie('Name', 'GarageSystem')
      return resp
      return redirect(url_for('homepage'))
      #return homepage()
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    res = make_response("Computer de-authorised")
    res.set_cookie('Name', 'None', max_age=0)
    return res  
    

@app.route("/", methods=['GET'])
def homepage():
  #print("got here3")
  message=""
  try:
    name = request.cookies.get('Name')
    if name == None:
      #return login()
      return redirect(url_for('login'))
      
    else:
      data = request.args
      searchString = buildSearchString(data)
      invoiceHeaders = getInvoiceHeaders(searchString)
      
      totals = getInvoiceHeadersTotal(searchString)
      
      datelastupdated = getLastUpdate()
      print("got here h1")
      try:
        flgEstimates=data["estimates"]
      except:
        flgEstimates=""
      if flgEstimates=="estimates" and data["datetypevalue"]=="Paid":
        message = "You have asked for paid estimates - you may want to consider setting the date type to 'IN'"
      print("got here h2")
      #print("*** date last updated ***")
      #print(datelastupdated[1])
      return render_template('home.html',message=message,
                             searchstring=searchString,
                             data=data,
                             invoiceheaders=invoiceHeaders,
                             totals=totals,
                             datelastupdated=datelastupdated
                            )
  except:
    message = "*** Message in except clause of homepage in App.py - No search criteria ***"
    return render_template('home.html', data=data, message=message)


@app.route("/invoice/<ID>")
def loadInvoice(ID):
  print("got here2")
  invoiceHeader = getInvoiceHeader(ID)
  parts=getParts(ID)
  work=getWork(ID)
  return render_template('invoiceheader.html', data=invoiceHeader, parts=parts, work=work)

@app.route("/diaryday")
def displayDiaryDayToday():
  Datestr=datetime.today().strftime("%Y-%m-%d")
  return displayDiaryDay(Datestr)

@app.route("/diaryday/<Datestr>")
def displayDiaryDay(Datestr):
  Date=datetime.strptime(Datestr, "%Y-%m-%d")
  bookings=getBookings(Datestr)
  return render_template('diaryday.html', date=Date.strftime("%a %d %B %Y"), dateiso=Datestr, bookings=bookings)

@app.route("/book")
def displayBookingForm():
  Datestr=datetime.today().strftime("%Y-%m-%d")
  return render_template('book.html')

@app.route("/book/<ID>")
def editBooking(ID):
  booking=getBooking(ID)
  return render_template('book.html', booking=booking)

@app.route("/savebooking", methods = ['POST'])
def saveBooking():
  if request.method=='POST':
    formdata=request.form
    ID = saveBookingToDB(formdata)
    return render_template('book.html', id=ID)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
