import sys
import usb.core
import usb.util
import serial

#To prevent the 'Error: The device has no langid' issue
#Must add the line below to the 99-*.rules file at: /etc/udev/rules.d
#SUBSYSTEM=="usb", MODE=="0666", GROUP=="usbusers"

#Open the USBLog and clear out the log
def clearLog():
    pop = 1

#Display each entry in the log
def displayLog():
    pop = 2

#These are the port numbers for the raspberry pi
PORT_NUMBER = [2, 3, 4, 5]

#-d is to display everything in the log
#-c is to clear the log
#-dc is to first display everything in the log and then clear the log
ALLOWED_ARGS = ["-d", "-c", "-dc" ]


def main():
    devs = usb.core.find(find_all=True)
    
    USBCount = 0
    try:
        logFile = open('USBLog', 'a+')
        
        logData = logFile.readlines()
        FoundID = False
        validParams = True
        
        paramSize = len(sys.argv)
        
        if paramSize == 1:
        
            for dev in devs:
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
                    FoundID = False
            
            #    print(str(dev.product) + ' by ' + str(dev.manufacturer)  + ', Decimal VID & PID = ' + str(dev.idVendor) + ' : ' + str(dev.idProduct) + " at port: " + str(dev.serial_number)  +  '\n')
        
        else:
            param = sys.argv[1]
            
            #This checks to see if the parameter passed is one of the allowed args. 
            #If so, then do the action that the arg correlates to
            #If not validParams = False and tells the user
            if not param in ALLOWED_ARGS:
                validParams = False
                print("Parameter entered are not valid.")
            else:
                print(param)
        
        if not USBCount and validParams:
            print("Nothing connected to USB Ports!")
    
    except ValueError as e:
        print(e)
        if e == "The device has no langid":
            print("This issue can possibly be fixed by going to the /etc/udev/rules.d directory and writing the following line in the 99-*.rules file")
            print("SUBSYSTEM==\"usb\", MODE==\"0666\", GROUP==\"usbusers\"")
     
    finally:
        logFile.close()


if __name__ == "__main__":
    main()


