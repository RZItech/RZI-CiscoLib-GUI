from netmiko import ConnectHandler
import tkinter as tk
from tkinter import ttk
import datetime
# Setup


device = { 
    "device_type": "cisco_ios",
    "host": "",
    "username": "",
    "password": "",
    "secret": "",
}

def get_license_data(C):
    _STDOUT_EN = C.run('en', pty=True)
    print("en outputed the following: "+_STDOUT_EN)
    _STDOUT_LICESNSE = C.run('show license', pty=True)
    print("sh license outputed the following: "+ _STDOUT_LICESNSE)
    return _STDOUT_LICESNSE

def cisco_get_perf_license() :
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
    f = open("OUT.txt","a")
    f.write("\n"+str(datetime.date.today())+"\n")

    for i in _INLIST :
        # Update the IP address each loop
        device.update({"host": i})
        
        # Start connection to cisco_ios device
        with ConnectHandler(**device) as net_connect:
            #Send "show license"
            net_connect.enable()
            output = net_connect.send_command("show license")
            if "PERF" in output.upper() :
                #If there is a performance license, return True
                perflicense = True
            else :
                # Otherwise, return False
                perflicense = False
            # Write to OUT.txt
            f.write("\n"+i+": Performance License = "+perflicense)
            # Close Connection
            net_connect.disconnect()


        


# Initilaze GUI
window = tk.Tk()

ttk.Label(text="RZI Cisco Data Collector").pack()

intxt = tk.Text(height=15, width=30)
intxt.pack()

userlabel = ttk.Label(window, text="User Name")
passwdlabel = ttk.Label(window, text="Password")
enpasswdlabel = ttk.Label(window, text="EN Password")
user = ttk.Entry(window)
passwd = ttk.Entry(window)
enpasswd = ttk.Entry(window)

userlabel.pack()
user.pack()
passwdlabel.pack()
passwd.pack()
enpasswdlabel.pack()
enpasswd.pack()


btn = ttk.Button(text="Get License Data", command=cisco_get_perf_license ,)
btn.pack()



window.mainloop()

