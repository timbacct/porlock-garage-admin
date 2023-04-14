from sqlalchemy import create_engine, text
#from flask import jsonify
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

#def getInvoiceHeadersFromDB():

#    with engine.connect() as conn:
#      result = conn.execute(text("SELECT * FROM InvoiceHeader"))
#      invoiceHeaders = []
#      for row in result.all():
#          invoiceHeaders.append(dict(row))
#      print(result.all())
#      return invoiceHeaders

def getInvoiceHeader(selection):
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "SELECT ID, CustomerName, InvoiceNumber, PhoneNumber,  DATE_FORMAT(DateIn, '%d.%m.%Y') AS DateIn, DateInJulian, MakeModel, ifnull(MakeModel2,'') AS MakeModel2, RegistrationNumber, Mileage, DATE_FORMAT(PaidDate, '%d.%m.%Y') AS PaidDate, ifnull(PaidDateJulian,0) AS PaidDateJulian, ifnull(PaymentType,'') AS PaymentType, Cashier, GarageOwner, PathName, FileName, ifnull(FileSize,0) AS FileSize, ifnull(MOTValue,0) AS MOTValue, ifnull(ListPartsTotal,0) AS ListPartsTotal, ifnull(ListLabourTotal,0) AS ListLabourTotal, ifnull(SummaryLabour,0) AS SummaryLabour, ifnull(SummaryLabourVAT,0) AS SummaryLabourVAT, ifnull(SummaryLabourTotal,0) AS SummaryLabourTotal, ifnull(SummaryMOT,0) AS SummaryMOT, ifnull(SummaryMOTVAT,0) AS SummaryMOTVAT, ifnull(SummaryMOTTotal,0) AS SummaryMOTTotal, ifnull(SummaryParts,0) AS SummaryParts, ifnull(SummaryPartsVAT,0) AS SummaryPartsVAT, ifnull(SummaryPartsTotal,0) AS SummaryPartsTotal, ifnull(SummaryPrice,0) AS SummaryPrice, ifnull(SummaryVAT,0) AS SummaryVAT, ifnull(SummaryTotal,0) AS SummaryTotal FROM InvoiceHeader WHERE ID = "
        + str(selection))).fetchone()
    return result


def getInvoiceHeaders(searchString):
  if searchString=="":
    pass
  else:
    with engine.connect() as conn:
      result = conn.execute(
        text(
          "SELECT CustomerName, InvoiceNumber, PhoneNumber, DateIn, PaidDate, MakeModel, RegistrationNumber, Mileage, SummaryPrice, SummaryTotal,ID, PathName, FileName FROM InvoiceHeader "
          + str(searchString) + " ORDER BY DateInJulian "))
    return result

def getInvoiceHeadersTotal(searchString):
  #print("******   searchString   *****")
  #print(searchString)
  if searchString=="":
    searchString=""
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "SELECT CONCAT('£',FORMAT(SUM(SummaryPrice),2,'en_US')) AS TotalExVAT, CONCAT('£',FORMAT(SUM(SummaryTotal),2,'en_US')) AS TotalIncVAT FROM InvoiceHeader "
        + str(searchString)))
    return result

#def dictify(funcName, searchString, jsonifyFlag):
#  match funcName:
#    case "getInvoiceHeaders":
#      result = getInvoiceHeaders("searchString")
#    case "getInvoiceHeader":
#      result = getInvoiceHeader(searchString)
#  dictifiedResult = []
#  for row in result.all():
#    print(result)
#    dictifiedResult.append(dict(row))
#  if jsonifyFlag=="Y":
#    return jsonify(dictifiedResult)
#  else:
#    return dictifiedResult



def getParts(selection):
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "SELECT Code AS PartsCode, CONCAT(description, ' ', description2) AS PartsDescription, Price AS PartsPrice, ID AS PartsID FROM Parts WHERE InvoiceHeaderID = "
        + str(selection))).fetchall()
    return result


def getWork(selection):
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "SELECT CONCAT(Description, ' ', Description2, ' ', Description3) AS WorkDescription, Price AS WorkPrice, ID AS WorkID FROM Work WHERE InvoiceHeaderID = "
        + str(selection))).fetchall()
    return result



def deleteInvoice(selection):
  with engine.connect() as conn:
    try:
      conn.execute("DELETE FROM Parts WHERE InvoiceHeaderID = " +
                   str(selection))
      rows = conn.fetchall()
      for row in rows:
        if row[0] == None:
          pass
        else:
          print(row[0])
      conn.execute("DELETE FROM Work WHERE InvoiceHeaderID = " +
                   str(selection))
      rows = conn.fetchall()
      for row in rows:
        if row[0] == None:
          pass
        else:
          print(row[0])
      conn.execute("DELETE FROM InvoiceHeader WHERE ID = " + str(selection))
      rows = conn.fetchall()
      for row in rows:
        if row[0] == None:
          pass
        else:
          print(row[0])
      conn.commit()
      print("Successfully deleted invoice from database")

    except Exception as e:
      print("Deleting invoice from database failed")
      print("DELETE FROM Parts WHERE InvoiceHeaderID = " + str(selection))
      print(repr(e))


def getLastUpdate():
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT MAX(date(DateInJulian)) FROM InvoiceHeader"))
  return result


def saveInvoiceHeaderToDB(
    name, invoiceNo, telephoneNo, dateIn, dateInJulian, makeModel, regNo,
    mileage, paidDate, paidDateJulian, paymentType, cashier, garageOwner,
    pathName, fileName, fileSize, MOTValue, listPartsTotal, listLabourTotal,
    summaryLabour, summaryLabourVAT, summaryLabourTotal, summaryMOT,
    summaryMOTVAT, summaryMOTTotal, summaryParts, summaryPartsVAT,
    summaryPartsTotal, summaryPrice, summaryVAT, summaryTotal):

  with engine.connect() as conn:

    conn.execute(
      text(
        "INSERT INTO InvoiceHeader (CustomerName, InvoiceNumber, PhoneNumber, DateIn, DateInJulian, MakeModel, RegistrationNumber, Mileage,  PaidDate, PaidDateJulian, PaymentType, Cashier,GarageOwner, PathName, FileName, FileSize, MOTValue, ListPartsTotal, ListLabourTotal, SummaryLabour, SummaryLabourVAT, SummaryLabourTotal,SummaryMOT, SummaryMOTVAT, SummaryMOTTotal, SummaryParts, SummaryPartsVAT, SummaryPartsTotal, SummaryPrice, SummaryVAT, SummaryTotal)VALUES ("
        + name + ", " + invoiceNo + ", " + telephoneNo + ", " + dateIn + ", " +
        dateInJulian + ", " + makeModel + ", " + regNo + ", " + mileage +
        ", " + paidDate + ", " + paidDateJulian + ", " + paymentType + ", " +
        cashier + ", " + garageOwner + ", " + pathName + ", " + fileName +
        ", " + fileSize + ", " + MOTValue + ", " + listPartsTotal + ", " +
        listLabourTotal + ", " + summaryLabour + ", " + summaryLabourVAT +
        ", " + summaryLabourTotal + ", " + summaryMOT + ", " + summaryMOTVAT +
        ", " + summaryMOTTotal + ", " + summaryParts + ", " + summaryPartsVAT +
        ", " + summaryPartsTotal + ", " + summaryPrice + ", " + summaryVAT +
        ", " + summaryTotal + ")"))
    conn.commit()
    result = conn.execute('select MAX(ID) from InvoiceHeader;')
    #print(cursor)
    return result.lastrowid
    #print(len(cursor.fetchall()))


def savePartsWorkToDB(part, work, invoiceHeaderID):

  with engine.connect() as conn:

    for item in part:

      insert_query = """INSERT INTO Parts
                                      (Code, Description, Description2, Price, InvoiceHeaderID) 
                                      VALUES (?, ?, ?, ?, ?);"""
      header = (item[0], item[1], item[2], item[3], invoiceHeaderID)

      conn.execute(insert_query, header)

    conn.commit()

    for item in work:

      insert_query = """INSERT INTO Work
                                      (Description, Description2, Description3, Price, InvoiceHeaderID) 
                                      VALUES (?, ?, ?, ?, ?);"""
      header = (item[0], item[1], item[2], item[3], invoiceHeaderID)
      #print(header)

      conn.execute(insert_query, header)

    conn.commit()


def checkFileLoaded(machineSensitiveRoot, pathName, fileName, fileSize):

  with engine.connect() as conn:

    #select_query = "SELECT FileSize, ID FROM InvoiceHeader WHERE PathName = '" + pathName + "' AND FileName = '" + fileName + "'"
    #header = (pathName, fileName)
    #print(header)
    #print(select_query)
    result = conn.execute(
      text("SELECT FileSize, ID FROM InvoiceHeader WHERE PathName = '" +
           pathName + "' AND FileName = '" + fileName + "'"))
    rows = result.fetchall()
    for row in rows:
      if len(row) > 0:
        # file exists.  Check if filesize is the same
        if row[
            0] == fileSize:  # file exists and is exactly the same size so probably unchanged
          result = True
        else:
          # File size is different.  It looks like the invoice file has been updated - delete the record
          delete_query = "DELETE FROM Work WHERE InvoiceHeaderID = " + str(
            row[1])
          conn.execute(delete_query)
          conn.commit()
          result = conn.execute("SELECT * FROM Work WHERE InvoiceHeaderID = " +
                                str(row[1]))
          morerows = result.fetchall()
          delete_query = "DELETE FROM PARTS WHERE InvoiceHeaderID =  " + str(
            row[1])
          conn.execute(delete_query)
          conn.commit()
          delete_query = "DELETE FROM InvoiceHeader WHERE ID =  " + str(row[1])
          conn.execute(delete_query)
          conn.commit()
          result = conn.execute("SELECT * FROM Work WHERE InvoiceHeaderID = " +
                                str(row[1]))
          morerows = result.fetchall()
          print("Found duplicate")
          # record has been deleted so needs to be loaded as if it had never been in the database
          result = False
      else:
        # file has not been imported
        result = False
