# go through directories pulling out invoice files and recording them on the database

import glob
from loadinvoicespreadsheetstotable import LoadInvoiceToDB
from loadinvoicespreadsheetstotable import *
from database import checkFileLoaded, getFileList
import os
import platform

paths = ("Documents/Aa Invoices/A-D/*.xls*",
         "Documents/Aa Invoices/E-H/*.xls*",
         "Documents/Aa Invoices/I-L/*.xls*",
         "Documents/Aa Invoices/M-R/*.xls*", 
         "Documents/Aa Invoices/S.W.Y/*.xls*")


def loadInvoices(machineSensitiveRoot):
    fileListFromDB = getFileList()
    for path in paths:
        #path holds the relative directory path and wildcard to search - thisis what we want to be stored against the invoice
        #pathName holds the relative directory path on its own
        #fullPath holds the full path to search as it is known on the current machine
        #fileNameAndPath holds the fully qualified file name and path as know on the current machine
        
        fullPath=machineSensitiveRoot + path
        pathName=path[:path.rfind(".")-1]

        print("Starting processing directory: " + pathName)

        for fileNameAndPath in glob.glob(fullPath):
            fileName=fileNameAndPath[fileNameAndPath.rfind("/")+1:]
            if fileName[fileName.rfind("."):]==".xls" or fileName[fileName.rfind("."):]==".xlsx":
                stats = os.stat(fileNameAndPath)
                fileSize = stats.st_size
                override=False
                if checkFileLoaded(fileListFromDB, machineSensitiveRoot, pathName, fileName, fileSize)==True and override==False:
                     pass
                else:
                    LoadInvoiceToDB(machineSensitiveRoot, pathName, fileName, fileSize)
            else:
                 pass
        print("Finished processing directory: " + pathName)