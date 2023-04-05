import socket
import time
import struct
import os
import customtkinter as ctk
#import tkinter as tk
import threading
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

#Open UDP socket
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


#formats of data loaded in
default_format = '<iI27f4i20f5i'

# Dash format (FM7)
dash_format = default_format + '17fH6B3b'

# Horizon format (FH4+)
horizon_format = default_format + 'i19fH6B4b'



unpacked = None
loopNum = 0
windowOpen = True

#Grabs the data from the UDP stream and unpacks it
def getData():
    global unpacked
    #for i in range(200):
    while windowOpen:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        unpacked = struct.unpack(horizon_format, data)


#Update the data visualization with a delay
def updateData():
    global unpacked
    global loopNum
    while windowOpen:
        loopNum += 1
        time.sleep(0.01)
        
        for i in range(len(unpacked)):
            stringVars[i].set("{:3d}: ".format(i) + str(unpacked[i]))





#Tkinter window setup
window = ctk.CTk()

scrollable = ctk.CTkScrollableFrame(
    window,
    width=600,
    height=800
)
scrollable.pack()

#Read one packet to get array size
data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
unpacked = struct.unpack(horizon_format, data)
stringVars = []
labels = []
for i in range(len(unpacked)):
    var = ctk.StringVar()
    stringVars.append(var)
    label = ctk.CTkLabel(
        scrollable,
        font=("Arial", 20),
        width=40,
        height=1,
        textvariable=var,
        anchor="w",
        justify=ctk.LEFT
    )
    label.grid(row=i, column=0, sticky="ew")
    labels.append(label)


#Start threads for getting and updating data
get = threading.Thread(target=getData)
get.start()

update = threading.Thread(target=updateData)
update.start()

window.mainloop()
windowOpen = False #Stop the UDP listening loop if the GUI window closes
print("lolbefore")
get.join()
update.join()
print("lolafter")