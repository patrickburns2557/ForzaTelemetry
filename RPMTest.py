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

#Grabs the data from the UDP stream and unpacks it
def getData():
    global unpacked
    #for i in range(200):
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        unpacked = struct.unpack(horizon_format, data)

#Update the data visualization with a delay
def updateData(frame=None):
    global unpacked
    global loopNum
    while True:
        loopNum += 1
        time.sleep(0.005)
        
        #update RPM in tkinter
        RPMVar.set("RPM: {:.0f}".format(unpacked[4]))
        print("RPM: " + "{:.0f}".format(unpacked[4]))
        print("list length: " + str(len(x)))
        print()

        #update RPM in graph
        x.append(loopNum)
        y.append(unpacked[4])
        #Remove oldest plot point after 500 datapoints
        if len(x) > 500:
            x.pop(0)
            y.pop(0)
        ln.set_data(x, y)
        
        #Move the graph horizonatally as points are plotted
        plt.xlim(loopNum-200, loopNum)
        
        #Update the upper limit of RPM graph based on the car you're driving
        if(unpacked[2] > 100):
            plt.ylim(0, unpacked[2]+500)
        
        return ln






#Tkinter window setup
window = tk.Tk()
RPMVar = tk.StringVar(value="0.0")
RPMLabel = tk.Label(
    window,
    font=("Arial", 20),
    width=40,
    height=3,
    textvariable=RPMVar,
    anchor="w",
    justify=tk.LEFT
)
RPMLabel.pack()

#Start threads for getting and updating data
get = threading.Thread(target=getData)
get.start()
update = threading.Thread(target=updateData)
update.start()

x = []
y = []

#matplotlib plot to show graph on
fig = plt.figure()
ln, = plt.plot(x, y, marker="o", markersize=2, color="red")

plt.ylim(0, 12000)

animation = FuncAnimation(fig, updateData, interval=1)
plt.show()
window.mainloop()


    

print()