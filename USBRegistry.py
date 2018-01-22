import sys
import os
import usb.core

#sys.path.insert(0, os.path.realpath('./USBRegOps.py'))
import USBRegOps

#To prevent the 'Error: The device has no langid' issue
#Must add the line below to the 99-*.rules file at: /etc/udev/rules.d
#SUBSYSTEM=="usb", MODE=="0666", GROUP=="usbusers"

#These are the USB port numbers for the Raspberry Pi 3 Model B
PORT_NUMBERS = [2, 3, 4, 5]

#-d is to display everything in the log
#-ld is to log the devices connected now and then display the log
#-c is to clear the log
#-dc is to first display everything in the log and then clear the log
#-ldc is to log the devices connected now, then display the log, and then clear the log
ALLOWED_ARGS = ["-d", "-ld", "-c", "-dc", "-ldc" ]


def main():
    devs = usb.core.find(find_all=True)
    
    try:
        #This gets the parameter the user may have passed
        #If no parameter is passed, then the IndexError is raised and the primary function will run in the except
        #EAFP
        param = sys.argv[1]
            
        #This checks to see if the parameter passed is one of the allowed args. 
        #If so, then do the action that the arg correlates to
        #If not validParams = False and tells the user
        if not param in ALLOWED_ARGS:
            print("Parameter entered are not valid.")
        else:
            USBRegOps.callParamTree(param, devs, PORT_NUMBERS)
        
    except IndexError as e:
        #Seeing as there are no parameters, we want just the basic functionality of adding any
        #unregistered devices to the log
        #Since this is the only time we deal with lists that can cause this error
        #Here we make params = None
        USBRegOps.callParamTree(None, devs, PORT_NUMBERS)

    except ValueError as e:
        print(e)
        if e == "The device has no langid":
            print("This issue can possibly be fixed by going to the /etc/udev/rules.d directory and writing the following line in the 99-*.rules file")
            print("SUBSYSTEM==\"usb\", MODE==\"0666\", GROUP==\"usbusers\"")


if __name__ == "__main__":
    main()


