import socket
import time
import datetime
import struct
import os
import tkinter as tk
import customtkinter as ctk
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

MSEC_TO_MPH = 2.236936


unpacked = None
loopNum = 0
windowOpen = True
FONT = ("Consolas", 15)


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
        time.sleep(0.001)
        
        #only update info when game is unpaused
        if unpacked[0] == 1:
            RPMVar.set("RPM: {:.0f}".format(unpacked[4]))
            GearVar.set("Gear: " + str(unpacked[84]))
            SpeedVar.set("Speed: {:>3.0f} MPH".format(unpacked[64]*MSEC_TO_MPH))
            RaceTimeVar.set("Time: " + str(datetime.timedelta(seconds=unpacked[77]))[:-4])
            CurrLapVar.set("Current Lap: " + str(datetime.timedelta(seconds=unpacked[76]))[:-4])
            BestLapVar.set("Best Lap: " + str(datetime.timedelta(seconds=unpacked[74]))[:-3])
            PrevLapVar.set("Last Lap: " + str(datetime.timedelta(seconds=unpacked[75]))[:-3])
            try:
                RPMBar.set(unpacked[4] / unpacked[2])
            except ZeroDivisionError:
                pass
            if RPMBar.get() > 0.9:
                RPMBar.configure(progress_color="red")
            else:
                RPMBar.configure(progress_color="#1f6aa5")




rowNum = 0

#Tkinter window setup
window = tk.Tk()
RPMVar = tk.StringVar(value="0.0")
RPMLabel = tk.Label(window, font=FONT, width=40, height=1, textvariable=RPMVar, anchor="w", justify=tk.LEFT)
RPMLabel.grid(row=rowNum, column=0, sticky="ew")
rowNum += 1

GearVar = tk.StringVar(value="0.0")
GearLabel = tk.Label(window, font=FONT, width=40, height=1, textvariable=GearVar, anchor="w", justify=tk.LEFT)
GearLabel.grid(row=rowNum, column=0, sticky="ew")
rowNum += 1

SpeedVar = tk.StringVar(value="0.0")
SpeedLabel = tk.Label(window, font=FONT, width=40, height=1, textvariable=SpeedVar, anchor="w", justify=tk.LEFT)
SpeedLabel.grid(row=rowNum, column=0, sticky="ew")
rowNum += 1

RaceTimeVar = tk.StringVar(value="0.0")
RaceTimeLabel = tk.Label(window, font=FONT, width=40, height=1, textvariable=RaceTimeVar, anchor="w", justify=tk.LEFT)
RaceTimeLabel.grid(row=rowNum, column=0, sticky="ew")
rowNum += 1

CurrLapVar = tk.StringVar(value="0.0")
CurrLapLabel = tk.Label(window, font=FONT, width=40, height=1, textvariable=CurrLapVar, anchor="w", justify=tk.LEFT)
CurrLapLabel.grid(row=rowNum, column=0, sticky="ew")
rowNum += 1

BestLapVar = tk.StringVar(value="0.0")
BestLapLabel = tk.Label(window, font=FONT, width=40, height=1, textvariable=BestLapVar, anchor="w", justify=tk.LEFT)
BestLapLabel.grid(row=rowNum, column=0, sticky="ew")
rowNum += 1

PrevLapVar = tk.StringVar(value="0.0")
PrevLapLabel = tk.Label(window, font=FONT, width=40, height=1, textvariable=PrevLapVar, anchor="w", justify=tk.LEFT)
PrevLapLabel.grid(row=rowNum, column=0, sticky="ew")
rowNum += 1

RPMBar = ctk.CTkProgressBar(window, width=500, height=23, corner_radius=3)
RPMBar.grid(row=rowNum, column=0, sticky="ew", padx=5, pady=5)
rowNum += 1



#Start threads for getting and updating data
get = threading.Thread(target=getData)
get.start()
update = threading.Thread(target=updateData)
update.start()

window.mainloop()
windowOpen = False