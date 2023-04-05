import socket
import time
import struct
import os
import tkinter as tk
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
def updateData(frame=None):
    global unpacked
    global loopNum
    while windowOpen:
        loopNum += 1
        time.sleep(0.05)

        #Only update the position plot while driving around
        if unpacked[0] != 0:
            x.append(unpacked[61])
            y.append(unpacked[63])#Use game's Z coord for the Y plot because Y in FH5 = elevation rather than Z
            ln.set_data(x, y)

            #Adjust the bounds of the graph to show the entire plot as it's drawn
            plt.xlim(min(x) - 100, max(x) + 100)
            plt.ylim(min(y) - 100, max(y) + 100)
        return ln





#Start threads for getting and updating data
get = threading.Thread(target=getData)
get.start()
update = threading.Thread(target=updateData)
update.start()

x = []
y = []

#matplotlib plot to show graph on
fig = plt.figure()
ln, = plt.plot(x, y, marker="o", markersize=2, color="blue")


animation = FuncAnimation(fig, updateData, interval=1)
plt.show()
windowOpen = False
