from database import getInvoiceHeaders, deleteInvoice, getLastUpdate

def displayMessage(message):
    messageBox.insert(INSERT,message + "\r")


def viewInvoiceHeaders(data):

    searchString = buildSearchString()
    #print("******   searchString   *****")
    #print(searchString)
    invoiceHeaders = getInvoiceHeaders(searchString)    
    totalValue()

def totalValue(item=""):
    total=0
    for child in tree.get_children():
        total=total + float(tree.item(child)["values"][8][1:])
    print(total)
    totalString="£{:,.2f}".format(total)
    invoiceTotal.delete(0,END)
    invoiceTotal.insert(0,totalString)
    total=0
    for child in tree.get_children():
        total=total + float(tree.item(child)["values"][9][1:])
    print(total)
    totalString="£{:,.2f}".format(total)
    invoiceTotalIncVAT.delete(0,END)
    invoiceTotalIncVAT.insert(0,totalString)
    


def getDateLastUpdated():
    dateLastUpdated.delete(0,END)
    displayDate=guessDateFormat(getLastUpdate())
    #print (displayDate.strftime("%d/%m/%Y"))
    dateLastUpdated.insert(0,displayDate.strftime("%d/%m/%Y"))





    
def buildSearchString():
    searchString=""
    #print("2nd one" + searchString=="")

    customerNameVal = customerName.get()
    registrationNumberVal = registrationNumber.get()
    dateInVal = dateIn.get()
    makeModelVal = makeModel.get()
    phoneNumberVal = phoneNumber.get()
    
    if customerNameVal != "":
        searchString = addSearchCriterionToString(searchString, "CustomerName", str(customerNameVal))
    if registrationNumberVal != "":
        searchString = addSearchCriterionToString(searchString, "RegistrationNumber", str(registrationNumberVal))
    if dateInVal != "":
        searchString = addSearchCriterionToString(searchString, "DateIn", str(dateInVal))
    if makeModelVal != "":
        searchString = addSearchCriterionToString(searchString, "MakeModel", str(makeModelVal))
    if phoneNumberVal != "":
        searchString = addSearchCriterionToString(searchString, "PhoneNumber", str(phoneNumberVal))
    #searchString = addDateRangeToString(searchString)
    searchString = addDateAndTypeRangeToString(searchString)
    searchString = addCheckbuttonCriteriaToString(searchString)
    print(searchString)
    return searchString

def addSearchCriterionToString(searchString, column, value):
    if searchString == "":
        searchString = "WHERE " + column + " LIKE '%" + value + "%'"
        #print("1 " + searchString)
    else:
        searchString = searchString + " AND " + column + " LIKE '%" + value + "%'"
        #print("2 " + searchString)
    return searchString

def addCheckbuttonCriteriaToString(searchString):
    flgEstimateValue=flgEstimates.get()
    flgInvoicesValue=flgInvoices.get()
    if flgEstimateValue==0 and flgInvoicesValue==0:
        flagString = "InvoiceNumber = 'asdfasdfasdfsdfsafaf;"
    if flgEstimateValue==0 and flgInvoicesValue==1:
        flagString = "InvoiceNumber NOT LIKE 'Estimate'"
    if flgEstimateValue==1 and flgInvoicesValue==0:
        flagString = "InvoiceNumber = 'Estimate'"
    if flgEstimateValue==1 and flgInvoicesValue==1:
        flagString = ""
    if flagString=="":
        pass
    else:
        if searchString == "":
            searchString = "WHERE " + flagString
            #print("1 " + searchString)
        else:
            searchString = searchString + " AND " + flagString
            #print("2 " + searchString)
    return searchString


def getStartAndEndOfPeriod(period):
    if period == "Week":
        dayNo = dt.weekday()
        startOfPeriod = dt - relativedelta(days = dayNo)
        endOfPeriod = dt + relativedelta(days = 6 - dayNo)
    if period == "Month":
        startOfPeriod = "1/" + str(dt.month) + "/" + str(dt.year)
        res = calendar.monthrange(dt.year, dt.month)
        endOfPeriod = str(res[1]) + "/" + str(dt.month) + "/" + str(dt.year)
        startOfPeriod=datetime.strptime(startOfPeriod, ("%d/%m/%Y"))
        endOfPeriod=datetime.strptime(endOfPeriod, ("%d/%m/%Y"))
    if period == "Year":
        startOfPeriod = "1/1/" + str(dt.year)
        endOfPeriod = "31/12/" + str(dt.year)
        startOfPeriod=datetime.strptime(startOfPeriod, ("%d/%m/%Y"))
        endOfPeriod=datetime.strptime(endOfPeriod, ("%d/%m/%Y"))
    print(str(startOfPeriod) + str(endOfPeriod))
    return startOfPeriod, endOfPeriod

def addDateAndTypeRangeToString(searchString):
    dateString=""
    dateStartVal = guessDateFormat(dateStart.get())
    dateEndVal=guessDateFormat(dateEnd.get())
    if dateStartVal==None and dateEndVal==None:
        return searchString
    print(str(dateStartVal) +  str(dateEndVal))
    if buttonDate.config('text')[-1] == "Paid":
        columnName="PaidDateJulian"
    else:
        columnName="DateInJulian"
    if dateStart =="":
        if dateEnd =="":
            # no range - drop out
            pass
        else:
            # date before end date
            dateString=columnName + " < TO_DAYS('" + dateEndVal.strftime('%Y-%m-%d') + "') + 1721060 "
    else:
        if dateEnd =="":
            dateString=columnName + " > TO_DAYS('" + dateEndVal.strftime('%Y-%m-%d') + "') + 1721060 "
        else:
            # date between beginning and end date
            dateString=columnName + " BETWEEN TO_DAYS('" + dateStartVal.strftime('%Y-%m-%d') + "' + 1721060 ) AND TO_DAYS('" + dateEndVal.strftime('%Y-%m-%d') + "') + 1721060  "
    print("In date and type" + searchString)
    if searchString == "":
        searchString = "WHERE " + dateString
    else:
        searchString = searchString + " AND " + dateString
    return searchString

def setDateFields():
    rbSelection=timeScope.get()
    match rbSelection:
        case 1: # All
            startOfPeriod=""
            endOfPeriod=""
        case 2:# Today
            dt=datetime.today()
            startOfPeriod=dt
            endOfPeriod=startOfPeriod
        case 3:# This week
            startOfPeriod, endOfPeriod=getStartAndEndOfPeriod("Week")
        case 4:# This month
            startOfPeriod, endOfPeriod=getStartAndEndOfPeriod("Month")
        case 5:# This year
            startOfPeriod, endOfPeriod=getStartAndEndOfPeriod("Year")
    dateStart.delete(0,END)
    dateEnd.delete(0,END)
    if rbSelection==1:
        dateStart.insert(0,"")
        dateEnd.insert(0,"")
    else:
        dateStart.insert(0,startOfPeriod.strftime("%d/%m/%Y"))
        dateEnd.insert(0,endOfPeriod.strftime("%d/%m/%Y"))

def addDateRangeToString(searchString):
    dateString = ""
    #dateStart.delete(0,END)
    #dateEnd.delete(0,END)
    match timeScope.get():
        case 1:
            dateString = ""
        case 2:
            dateString = " DateInJulian = julianday(date('now')) "
            #dateStart.insert(0,datetime.today())
            #dateEnd.insert(0,datetime.today())
        case 3:
            startOfPeriod, endOfPeriod = getStartAndEndOfPeriod("Week")
            dateString = " DateInJulian BETWEEN julianday('" + startOfPeriod.strftime('%Y-%m-%d') + "') AND julianday('" + endOfPeriod.strftime('%Y-%m-%d') + "')"
            #dateStart.insert(0,startOfPeriod)
            #dateEnd.insert(0,endOfPeriod)
        case 4:
            startOfPeriod, endOfPeriod = getStartAndEndOfPeriod("Month")
            #dateStart.insert(0,startOfPeriod)
            #dateEnd.insert(0,endOfPeriod)
            #dateString = " DateInJulian BETWEEN julianday(date('now', 'start of month')) AND julianday(date('now'))"
        case 5:
            #startOfPeriod, endOfPeriod = getStartAndEndOfPeriod("Year")
            #dateStart.insert(0,startOfPeriod)
            #dateEnd.insert(0,endOfPeriod)
            dateString = " DateInJulian BETWEEN julianday(date('now', 'start of year')) AND julianday(date('now'))"
    if dateString == "":
        pass
    else:
        if searchString == "":
            searchString = "WHERE " + dateString
        else:
            searchString = searchString + " AND " + dateString
    print(searchString)
    return searchString


def updateDatabase():
    LI.loadInvoices(machineSensitiveRoot)
    getDateLastUpdated()
    print("Updated")
    viewInvoiceHeaders()


def guessDateFormat(inputDate):
    date_patterns = ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y"]
    print(inputDate)
    for pattern in date_patterns:
        try:
            return datetime.strptime(inputDate, pattern).date()
        except:
            pass

    print ("Date is not in expected format: %s" + inputDate)

def viewInvoiceHeaders():
    for item in tree.get_children():
        tree.delete(item)
    tree.grid(row=0, column=0)
    searchString = buildSearchString()
    #print("******   searchString   *****")
    #print(searchString)
    rows = getInvoiceHeaders(searchString)    
    for row in rows:
        #print(row) 
        tree.insert("", END, values=row)
    totalValue()
