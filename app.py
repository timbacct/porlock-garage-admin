from flask import Flask, render_template, request
from buttonhandlers import *
from database import getInvoiceHeaders, getInvoiceHeader, getInvoiceHeadersTotal, getParts, getWork
from logic import *

app = Flask(__name__)

INVOICEHEADERS = [{
  'id': 1,
  'customername': 'Fred',
  'invoicenumber': 123445,
  'phonenumber': '01643 847322'
}, {
  'id': 2,
  'customername': 'Jim',
  'invoicenumber': 125645,
  'phonenumber': '01643 123443'
}, {
  'id': 3,
  'customername': 'Jo',
  'invoicenumber': 84884,
  'phonenumber': '01643 453454'
}]

INVOICEHEADER = [{
  'id': 2,
  'customername': 'Jim',
  'invoicenumber': 125645,
  'phonenumber': '01643 123443'
}]

#@app.route("/")
#def homepage():
#  return render_template('home.html')


@app.route("/", methods=['GET'])
def homepage():
  try:
    data = request.args
    
    searchString = buildSearchString(data)
    invoiceHeaders = getInvoiceHeaders(searchString)
    totals = getInvoiceHeadersTotal(searchString)
    return render_template('home.html',
                           searchstring=searchString,
                           data=data,
                           invoiceheaders=invoiceHeaders,
                           totals=totals)
  except:
    message = "*** Message in except clause of homepage in App.py - No search criteria ***"
    return render_template('home.html', data=data, message=message)


@app.route("/invoice/<ID>")
def loadInvoice(ID):
  invoiceHeader = getInvoiceHeader(ID)
  parts=getParts(ID)
  work=getWork(ID)
  return render_template('invoiceheader.html', data=invoiceHeader, parts=parts, work=work)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
