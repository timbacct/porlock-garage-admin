from flask import Flask, render_template

app = Flask(__name__)

INVOICEHEADERS = [
  {
    'id': 1,
    'customername': 'Fred',
    'invoicenumber': 123445,
    'phonenumber': '01643 847322'
  },
  {
    'id': 2,
    'customername': 'Jim',
    'invoicenumber': 125645,
    'phonenumber': '01643 123443'
  },
  {
    'id': 3,
    'customername': 'Jo',
    'invoicenumber': 84884,
    'phonenumber': '01643 453454'
  }
    ]


@app.route("/")
def hello_world():
  
  return render_template('home.html', invoiceheaders=INVOICEHEADERS)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
