def displayMessage(message):
    messageBox.insert(INSERT,message + "\r")

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

def openDetailWindow(Event):
    selectedItem = tree.selection()[0]
    selection=tree.item(selectedItem)['values'][10]
    print(str(selection))
    invoice=DisplayingInvoice.windows()
    invoice.showDetails(selection)
   

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



def clearFilters():
    customerName.delete(0,END)
    registrationNumber.delete(0,END)
    dateIn.delete(0,END)
    makeModel.delete(0,END)
    phoneNumber.delete(0,END)
    dateStart.delete(0,END)
    dateStart.insert(0,"")
    dateEnd.delete(0,END)
    dateEnd.insert(0,"")
    timeScope.set(1)
    buttonDate.config(text='In')
    flgEstimates.set(0)
    chkInvoices.select()

def openNewInvoice():
    invoiceType=cmbInvoiceType.get()
    print('open "' + machineSensitiveRoot + invoiceType + ' master.xltx"')
    os.system('open "' + machineSensitiveRoot + "Documents/Aa Invoices/Masters/" + invoiceType + ' master.xltx"')

def enterPressed(event):
    viewInvoiceHeaders()

def updateDatabase():
    LI.loadInvoices(machineSensitiveRoot)
    getDateLastUpdated()
    print("Updated")
    viewInvoiceHeaders()

def toggleDateSlider():
    
    if buttonDate.config('text')[-1] == 'In':
        buttonDate.config(text='Paid')
    else:
        buttonDate.config(text='In')
        

def dayEarlier():
    
    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(days=-1)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(days=-1)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))


def dayLater():

    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(days=1)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(days=1)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))

def weekEarlier():

    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(days=-7)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(days=-7)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))

def weekLater():

    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(days=7)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(days=7)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))


def monthEarlier():

    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(months=-7)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(months=-7)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))


def monthLater():

    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(months=7)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(months=7)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))


def yearEarlier():

    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(years=-7)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(years=-7)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))

def yearLater():

    newStartDate=datetime.strptime(dateStart.get(), "%d/%m/%Y") + timedelta(years=7)
    dateStart.delete(0,END)
    dateStart.insert(0,datetime.strftime(newStartDate, "%d/%m/%Y"))
    
    print(datetime.strptime(dateEnd.get(), "%d/%m/%Y"))
    newEndDate=datetime.strptime(dateEnd.get(), "%d/%m/%Y") + timedelta(years=7)
    print(newEndDate)
    
    dateEnd.delete(0,END)
    dateEnd.insert(0,datetime.strftime(newEndDate , "%d/%m/%Y"))