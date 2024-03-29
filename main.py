from netmiko import ConnectHandler
import tkinter as tk
from tkinter import ttk
import datetime
# Setup

job = 0

device = { 
    "device_type": "cisco_ios",
    "ip": "",
    "username": "",
    "password": "",
    "secret": "",
}



def cisco_wrmem() :
    # Define temporary variables
    _INPUTEXT = intxt.get("1.0",'end-1c')
    _INLIST = _INPUTEXT.split("\n")
    USER = user.get()
    PASSWD = passwd.get()
    EN = enpasswd.get()
    device.update({"username": USER})
    device.update({"password": PASSWD})
    device.update({"secret": EN })

    # Update OUT.txt
    print(USER+" "+PASSWD)
    f = open("wrmem.txt","a")
    f.write("\n"+str(datetime.date.today())+"\n")

    job = 0
    lenlist = len(_INLIST)
    for i in _INLIST :
        # Update the IP address each loop
        device.update({"ip": i})
        print("CONNECTING TO:"+i)
        # Start connection to cisco_ios device
        try :
            with ConnectHandler(**device) as net_connect:
                #Send "show license"
                net_connect.enable()
                wrmemout = net_connect.send_command("wr mem")

                print("wr mem OUT: \n"+wrmemout+"\n END")

                if "OK" in wrmemout.upper() :
                    #If there is a performance license, return True
                    f.write("\n"+i+": WR MEM Succeeded")
                    print("WR MEM DONE")

                else :
                    # Otherwise, return False
                    f.write("\n"+i+": WR MEM FAILED WITH OUTPUT : \n"+wrmemout+"\n")
                    print("WR MEM FAILED")

                # Close Connection
                net_connect.disconnect()
                print("CONNECTION CLOSED")
        
        except :
            print("ERROR CONNECTING TO "+i+", SKIPPING ...")
            


        


# Initilaze GUI
window = tk.Tk()

ttk.Label(text="RZI Mass WR MEM").pack()

intxt = tk.Text(height=15, width=30)
intxt.pack()

userlabel = ttk.Label(window, text="User Name")
passwdlabel = ttk.Label(window, text="Password")
enpasswdlabel = ttk.Label(window, text="EN Password")
user = ttk.Entry(window)
passwd = ttk.Entry(window)
enpasswd = ttk.Entry(window)

joblabel = ttk.Label(window, textvariable=job)

userlabel.pack()
user.pack()
passwdlabel.pack()
passwd.pack()
enpasswdlabel.pack()
enpasswd.pack()
joblabel.pack()


btn = ttk.Button(text="wr mem", command=cisco_wrmem ,)
btn.pack()



window.mainloop()

