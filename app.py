from flask import Flask, render_template
from database import dictify
from buttonhandlers from *
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


@app.route("/", methods=['post'])
def homepage():
  data = request.form
  invoiceHeaders = viewInvoiceHeaders(data)
  return render_template('home.html', invoiceheaders=invoiceHeaders)


@app.route("/invoiceheaders")
def exportInvoiceHeaders():
  return dictify("getInvoiceHeaders", "", "Y")


@app.route("/invoiceheader/<ID>")
def loadInvoiceHeader(ID):
  #invoiceHeader = dictify("getInvoiceHeader", ID, "N")
  return render_template('invoiceheader.html', invoiceheader =INVOICEHEADER[0])


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
