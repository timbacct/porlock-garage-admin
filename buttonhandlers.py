from logic import viewInvoiceHeaders
from loadinvoicesfromsubdirectory import loadInvoices
import os

def openSpreadsheet():
    selectedItem = tree.selection()[0]
    selectedPath=tree.item(selectedItem)['values'][11]
    pathName=selectedPath[selectedPath.find("documents"):]
    selectedFile=tree.item(selectedItem)['values'][12]
    print('open "' + machineSensitiveRoot +  selectedPath.strip() + selectedFile.strip() + '"')
    os.system('open "' + machineSensitiveRoot +  selectedPath.strip() + selectedFile.strip() + '"')

def motInfo():
    selectedItem = tree.selection()[0]
    selectedReg=tree.item(selectedItem)['values'][6]
    os.system('open https://cartaxcheck.co.uk/free-car-check/?vrm=' + selectedReg.strip())

def deleteSpreadsheet():
    selectedItem = tree.selection()[0]
    selectedPath=tree.item(selectedItem)['values'][11]
    pathName=selectedPath[selectedPath.find("documents"):]
    selectedFile=tree.item(selectedItem)['values'][12]
    print('"' + machineSensitiveRoot +  selectedPath.strip() + selectedFile.strip() + '"')
    try:
        os.remove('"' + machineSensitiveRoot +  selectedPath.strip() + selectedFile.strip() + '"')
    except Exception as e:
        print(repr(e))
        print("Deleting spreadsheet from directory failed")
   
def deleteSelectedInvoice():
    selectedItem = tree.selection()[0]
    selection=tree.item(selectedItem)['values'][10]
    deleteInvoice(selection)
    try:
        deleteSpreadsheet()
        print("Successfully deleted file from directory")
    except:
        print("Deleting invoice from directory failed")
    viewInvoiceHeaders()


def openNewInvoice():
    invoiceType=cmbInvoiceType.get()
    print('open "' + machineSensitiveRoot + invoiceType + ' master.xltx"')
    os.system('open "' + machineSensitiveRoot + "Documents/Aa Invoices/Masters/" + invoiceType + ' master.xltx"')

def enterPressed(event):
    viewInvoiceHeaders()

def updateDatabase():
  directoryRoot = "???????????????"
  loadInvoices(directoryRoot)
  #getLastUpdate()
  #print("Updated")
  #viewInvoiceHeaders()

        

