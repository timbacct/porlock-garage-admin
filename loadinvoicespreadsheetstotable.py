import pandas as pd
from database import saveInvoiceHeaderToDB, savePartsWorkToDB
from datetime import datetime


def infoBeside(df,x,y):
    return cleanCell(df.iat[x,y+1])

def infoBelow(df,x,y,count):
    if count == 2:
        return cleanCell(df.iat[x+1,y])+" "+cleanCell(df.iat[x+2,y])
    else: 
        return cleanCell(df.iat[x+1,y])

def infoBehind(df,x,y):
    return cleanCell(df.iat[x,y-1])

def cleanCell(value):
    value=str(value)
    if value=="nan":
        value=""
    return value

def cleanCellZero(value):
    value=str(value)
    if value=="nan" or value=="":
        value=0
    return value

def removeSpaces(value):
    value=value.replace(" ", "")
    return value
        
def formatDate(dateIn, pathName, fileName):
    try:
        if dateIn == "":
            pass
        else:
            if dateIn[0].isnumeric():
                dateIn = pd.to_datetime(dateIn, dayfirst=True).strftime("%Y/%m/%d")
                #print(dateIn)
                return dateIn
            else:
                pass
    except:
        print("Error in Date In in Worksheet " + pathName + fileName)
        print("dateIn was: " + dateIn + " first char is " + dateIn[0] + " check if numeric " + str(dateIn[0].isnumeric()))

def LoadInvoiceToDB(machineSensitiveRoot, pathName, fileName, fileSize):
    #print(fileName)
    # read by default 1st sheet of an excel file
    #print(machineSensitiveRoot + pathName+fileName)
    try:
        
        df = pd.read_excel(machineSensitiveRoot + pathName+fileName,header=None)

        #print(df)
        name=""
        invoiceNo=""
        telephoneNo=""
        dateIn=""
        dateInJulian=0
        makeModel=""
        regNo=""
        mileage=""
        paidDate=""
        paidDateJulian=0
        paymentType=""
        cashier=""
        garageOwner=""
        MOTValue=0
        listPartsTotal=0
        listLabourTotal=0
        summaryLabour=0
        summaryLabourVAT=0
        summaryLabourTotal=0
        summaryMOT=0
        summaryMOTVAT=0
        summaryMOTTotal=0
        summaryParts=0
        summaryPartsVAT=0
        summaryPartsTotal=0
        summaryPrice=0
        summaryVAT=0
        summaryTotal=0
        rows, cols = (40, 4)
        part = [[0 for i in range(cols)] for j in range(rows)]
        work = [[0 for i in range(cols)] for j in range(rows)]

        for x in range(df.shape[0]):

            for y in range(df.shape[1]):

                cellValue = df.iat[x,y]

    
                match cellValue:
                    case "Name" | "Name:":
                        name=infoBelow(df,x,y,1)
                        #print(name)
                    case "Invoice No" | "Invoice No:" | "Invoice No.":
                        invoiceNo=infoBeside(df,x,y)
                        if invoiceNo=="Estimate" or invoiceNo=="ESTIMATE":
                            invoiceNo="Estimate"
                    case "Estimate" | "ESTIMATE":
                        invoiceNo="Estimate"
                    case "Telephone" | "Telephone:" | "Telephone number" | "Telephone number:" | "Telephone Number" | "Telephone Number:":
                        telephoneNo=infoBelow(df,x,y,1)
                    case "Date" | "Date:" | "Date in" | "Date in:":
                        dateIn=infoBelow(df,x,y,1)
                        if dateIn == "":
                            dateIn=infoBeside(df,x,y)
                            if dateIn=="Make/model":
                                dateIn=""
                        if dateIn==None or dateIn=="":
                            dateIn=""
                            dateInJulian=0
                            pass
                        else:
                            dateIn=formatDate(dateIn, pathName, fileName)
                            
                            try:
                                dateInDate= datetime.strptime(dateIn, '%Y/%m/%d')
                                dateInJulian=dateInDate.toordinal() + 1721424.5
                            except:
                                print("Something wrong with Date In in file: " + fileName)
                                dateInJulian=""     
                        #print(str(dateInJulian) + " converted: " + str(dateInJulian) + " dateIn: " + dateIn)
                        #dateInJulian=j.to_jd(dateIn)
                        #print("In case statement" + str(dateIn) + " " +  str(dateInJulian))
                    case "Make/model" | "Make/Model:":
                        makeModel=infoBelow(df,x,y,2)
                    case "Reg No" | "Reg No." | "Reg No:":
                        regNo=infoBelow(df,x,y,1)
                        regNo=removeSpaces(regNo)
                    case "Mileage" | "Mileage:":
                        mileage=infoBelow(df,x,y,1)
                    case "Paid date":
                        paidDate=infoBeside(df,x,y)
                        if paidDate=="": paidDate=infoBehind(df,x,y)
                        paidDate=formatDate(paidDate, pathName, fileName)
                        try:
                            paidDateDate=datetime.strptime(paidDate, '%Y/%m/%d')
                            paidDateJulian=paidDateDate.toordinal() + 1721424.5
                        except:
                            print("Something wrong with paid Date in file: " + fileName)
                            paidDateJulian=0
                        if paidDateJulian=="":
                            paidDateJulian=0
                    case "Payment type":
                        paymentType=infoBeside(df,x,y)
                        if paymentType=="": paymentType=infoBehind(df,x,y)
                    case "Cashier":
                        cashier=infoBeside(df,x,y)
                        if cashier=="": cashier=infoBehind(df,x,y)                    
                    case "Part Number": #Header stuff is done and now looking at the second part of the invoice with invoice lines and summary box
                        #collect the invoice lines for parts and rows and for the summary box
                        i=0
                        #x+i represents the current line being processed.
                        #So we have to go to the next line after the last to end the while loop
                        #print(df)
                        while df.iat[x+i-1,y+2] != "Total Parts" and i < 100:
                            part[i][0]=cleanCell(df.iat[x+i,y])
                            part[i][1]=cleanCell(df.iat[x+i,y+1])
                            part[i][2]=cleanCell(df.iat[x+i,y+2])
                            part[i][3]=cleanCell(df.iat[x+i,y+3])
                            work[i][0]=cleanCell(df.iat[x+i,y+4])
                            work[i][1]=cleanCell(df.iat[x+i,y+5])
                            work[i][2]=cleanCell(df.iat[x+i,y+6])
                            work[i][3]=cleanCell(df.iat[x+i,y+7])
                            
                            #print("Got to here 3")
                            
                            if fileName[-1]== "x":
                                #print(i,x,y)
                                #print(df)
                                #print(df.iat[x+i, y+5]=="Price", df.iat[x+i, y+6]=="VAT", df.iat[x+i, y+7]=="Total")
                                # it is an invoice since I took over in a .xlsx type file
                                if df.iat[x+i, y+6] == "MOT":
                                    MOTValue=round(df.iat[x+i, y+7],2)
                                if df.iat[x+i-1,y+2] == "Total Parts":
                                    listPartsTotal=round(df.iat[x+i-1, y+3],2)
                                if df.iat[x+i, y+5] == "Total" and df.iat[x+i, y+6]=="Labour":
                                    listLabourTotal=round(df.iat[x+i, y+7],2)
                                if df.iat[x+i, y+5]=="Price" and df.iat[x+i, y+6]=="VAT" and df.iat[x+i, y+7]=="Total":
                                    labourRowIndex = x+i+1
                                    summaryLabour=round(df.iat[labourRowIndex, y+5],2)
                                    summaryLabourVAT=round(df.iat[labourRowIndex, y+6],2)
                                    summaryLabourTotal=round(df.iat[labourRowIndex, y+7],2)
                                    motRowIndex=labourRowIndex+1
                                    summaryMOT=round(df.iat[motRowIndex, y+5],2)
                                    summaryMOTVAT=round(df.iat[motRowIndex, y+6],2)
                                    summaryMOTTotal=round(df.iat[motRowIndex, y+7],2)
                                    partsRowIndex=motRowIndex+1
                                    summaryParts=round(df.iat[partsRowIndex, y+5],2)
                                    summaryPartsVAT=round(df.iat[partsRowIndex, y+6],2)
                                    summaryPartsTotal=round(df.iat[partsRowIndex, y+7],2)
                                    totalRowIndex=partsRowIndex+2
                                    summaryPrice=round(df.iat[totalRowIndex, y+5],2)
                                    summaryVAT=round(df.iat[totalRowIndex, y+6],2)
                                    summaryTotal=round(df.iat[totalRowIndex, y+7],2)
                                    
                            else:
                                # it is an old style invoice in .xls type file
                                
                                if df.iat[x+i, y+5] == "MOT":
                                    try:
                                        MOTValue=round(df.iat[x+i, y+6],2)
                                    except:
                                        print("Something wrong with MOTValue in file: " + fileName)
                                if df.iat[x+i,y+2] == "Total Parts":
                                    listPartsTotal=round(df.iat[x+i, y+3],2)
                                if df.iat[x+i, y+4] == "Total" and (df.iat[x+i, y+5]=="Labour" or df.iat[x+i, y+5]=="labour"):
                                    try:
                                        listLabourTotal=round(df.iat[x+i, y+6],2)
                                    except:
                                        print("Something wrong with listLabourTotal in file: " + fileName)
                                if df.iat[x+i, y+5]=="Price" and df.iat[x+i, y+6]=="Price" and df.iat[x+i, y+7]=="Price":
                                    labourRowIndex = x+i+1
                                    summaryLabour=round(df.iat[labourRowIndex, y+5],2)
                                    summaryLabourVAT=round(summaryLabour*.2,2)
                                    summaryLabourTotal=round(summaryLabour+summaryLabourVAT,2)
                                    motRowIndex=labourRowIndex+1
                                    try:
                                        summaryMOT=round(df.iat[motRowIndex, y+6],2)
                                    except:
                                        print("Something wrong with Summary MOT in file: " + fileName)
                                    summaryMOTVAT=0
                                    summaryMOTTotal=round(summaryMOT,2)
                                    partsRowIndex=motRowIndex+1
                                    summaryParts=round(df.iat[partsRowIndex, y+5],2)
                                    summaryPartsVAT=round(summaryParts*.2,2)
                                    summaryPartsTotal=round(summaryParts+summaryPartsVAT,2)
                                    totalRowIndex=partsRowIndex+2
                                    summaryPrice=round(df.iat[totalRowIndex, y+5]+df.iat[totalRowIndex, y+6],2)
                                    summaryVAT=round(df.iat[totalRowIndex+1, y+5],2)
                                    summaryTotal=round(df.iat[totalRowIndex+2, y+7],2)
                            i+=1
        if fileName[-1]== "x":
            garageOwner="Tim"
        else:
            garageOwner="Jonty"

        MOTValue = cleanCellZero(MOTValue)
        listPartsTotal = cleanCellZero(listPartsTotal)
        listLabourTotal = cleanCellZero(listLabourTotal)
        summaryLabour = cleanCellZero(summaryLabour)
        summaryLabourVAT = cleanCellZero(summaryLabourVAT)
        summaryLabourTotal = cleanCellZero(summaryLabourTotal)
        summaryMOT = cleanCellZero(summaryMOT)
        summaryMOTVAT = cleanCellZero(summaryMOTVAT)
        summaryMOTTotal = cleanCellZero(summaryMOTTotal)
        summaryParts = cleanCellZero(summaryParts)
        summaryPartsVAT = cleanCellZero(summaryPartsVAT)
        summaryPartsTotal = cleanCellZero(summaryPartsTotal)
        summaryPrice = cleanCellZero(summaryPrice)
        summaryVAT = cleanCellZero(summaryVAT)
        summaryTotal = cleanCellZero(summaryTotal)
           

        invoiceHeaderID = saveInvoiceHeaderToDB(name, invoiceNo, telephoneNo, dateIn, dateInJulian, makeModel, regNo, mileage,
                paidDate, paidDateJulian, paymentType, cashier, garageOwner, pathName, fileName, fileSize,
                 MOTValue, listPartsTotal, listLabourTotal, summaryLabour, summaryLabourVAT, summaryLabourTotal, summaryMOT,
                summaryMOTVAT, summaryMOTTotal, summaryParts, summaryPartsVAT, summaryPartsTotal, summaryPrice, summaryVAT, summaryTotal)



        #print(invoiceHeaderID)
        savePartsWorkToDB(part, work, invoiceHeaderID)
        print("Successfully loaded: ")
        print(machineSensitiveRoot + pathName+fileName)


    except Exception as e:
        print(e)
        print("Error loading file: " + machineSensitiveRoot + pathName+fileName)
        print(machineSensitiveRoot)
        print(pathName)
        print(fileName)
                    


