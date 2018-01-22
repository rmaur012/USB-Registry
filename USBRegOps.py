import os

#To prevent the 'Error: The device has no langid' issue
#Must add the line below to the 99-*.rules file at: /etc/udev/rules.d
#SUBSYSTEM=="usb", MODE=="0666", GROUP=="usbusers"

#Open the USBLog and clear out the log
def clearLog():
    try:
        if os.stat('USBLog').st_size:
            open('USBLog', 'w').close()
            print("Log has been cleared!")
        else:
            print("Nothing to clear!")
    except:
        raise

#Display each entry in the log
def displayLog():
    try:
        logFile = open('USBLog', 'r')
        logData = list(logFile)

        #If there is at least 1 entry in the log, display all entries
        if len(logData):
            print("ID:Product:Manufacturer")
            print("____Log Entries___")
            for log in logData:
                print(log.rstrip('\n'))
        #Else, tell the user there are no entries
        else:
            print("The log is empty!")

    except:
        raise
    finally:
        logFile.close()


#Port numbers are passed from main
def logAndSeeConnectedDevices(devs, PORT_NUMBERS):
    USBCount = 0
    try:
        logFile = open('USBLog', 'a+')
        logFile.seek(0)
        logData = logFile.readlines()
        for dev in devs:
            FoundID = False
            #USB ports have port numbers 2, 3, 4 &  5
            if dev.port_number in PORT_NUMBERS:
                
                #1. Search Log to see if this device can be found in it. The ID is in the format: idVendor$idProduct
                DevLogID = str(dev.idProduct) + '^' + str(dev.idVendor)
                for line in logData:
                    logParts = line.split(":")
                    lineID = logParts[0]
                
                    #2. If device is found, display and state that it is registered.
                    if lineID == DevLogID:
                        FoundID = True
                        print(str(dev.product) + ' by '  + str(dev.manufacturer) + ' connected at USB port ' + str(dev.port_number)  + ". Device Already Logged.")
                        break
                            
                    #3. If not, register the device and display it. Noting that is has been saved. The format is= ID:Product:Vendor
                if not FoundID:
                    newEntry = DevLogID + ":" + dev.product + ":" + dev.manufacturer + "\n"
                    logFile.write(newEntry)
                    print(str(dev.product) + ' by ' + str(dev.manufacturer) + ' connected at USB port ' + str(dev.port_number) + ". Device Now Registered.")
        #           logData = logFile.readLines()
                
                USBCount = USBCount + 1


        if not USBCount:
            print("Nothing connected to USB Ports!")
    
    except:
        raise

    finally:
        logFile.close()

def callParamTree(param, devs, PORT_NUMBERS):

    if param is None:
        logAndSeeConnectedDevices(devs, PORT_NUMBERS)

    elif param == "-d":
        displayLog()

    elif param == "-ld":
        logAndSeeConnectedDevices(devs, PORT_NUMBERS)
        displayLog()
    
    elif param == "-c":
        clearLog()
    
    elif param == "-dc":
        displayLog()
        clearLog()
    
    elif param == "-ldc":
        logAndSeeConnectedDevices(devs, PORT_NUMBERS)
        displayLog()
        clearLog()

