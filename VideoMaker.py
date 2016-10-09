#===============================================================================
#= Vars ========================================================================
padding = 0.02           # Space between sqaures
font_size = 8

#animation
secs_till_delete = 3.0   # Time a sqaure remains on screen
grow_speed = 2.0         # Exponent of grow accel function
grow_time = 0.2          # Time it takes a sqaure to full size

#sqaures
width = 0.06
hight = 0.06
fillets = 0.004          # Size of the roundings of the corners
face_color = 'lightgrey' # Color of the keys
LineWidth = 0.5
#===============================================================================
#===============================================================================
from matplotlib import pyplot as plot
from numpy import loadtxt
import numpy as np
from matplotlib.patches import FancyBboxPatch as rBox
from matplotlib.patches import BoxStyle as bs
import KeysRecorded
import cv2
#===============================================================================
#Init
#===============================================================================
imgWH = 1200.0
Dpi = 200
FPS = 30
kr = KeysRecorded.values_recorded
ascii = loadtxt("KeyData.txt")
times = loadtxt("TimeData.txt")
writer = cv2.VideoWriter("KEYS.avi",-1,FPS,(480,480))


def decel_motion_path(t):
    if(t<0):
        return 0
    if(t<grow_time):
        return (1-((1-(1.0/grow_time)*t)**grow_speed))
    else:
        return 1

def plot_and_save(figNum,time):
    #===========================================================================
    #init
    #===========================================================================
    plot.ioff()
    fig = plot.figure(1,facecolor = "lime",figsize = (imgWH/Dpi,imgWH/Dpi))
    curr_time , curr_ascii = get_data_from(time)
    yOffset = 0.1
    plot.axis("off")
    #===========================================================================
    #draw plot
    #===========================================================================
    for j in range(len(curr_time)):
        i = len(curr_time)-j-1
        multiplier = decel_motion_path(time-curr_time[i])
        w = width*multiplier
        h = hight*multiplier
        p = padding*multiplier
        xpos = width - 0.5*w
        ypos = yOffset #+h

        string = ""
        for k in kr:
            if(curr_ascii[i] == k[0]):
                string = k[1]
                break

        box = rBox([xpos,ypos],
                    w,
                    h,
                    boxstyle=bs("Round", pad=fillets),
                    facecolor=face_color,
                    linewidth = LineWidth)
        currentAxis = plot.gca()
        currentAxis.add_patch(box)
        if font_size*multiplier>=1:
            plot.text(  xpos+0.5*w,
                        ypos+0.5*h,
                        string,
                        va="center",
                        ha="center",
                        size=font_size*multiplier)

        yOffset+=h+p

    #===========================================================================
    # Add the plot to the vid
    #===========================================================================
    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    writer.write(data)

    plot.clf()
    return

def get_data_from(time):
    tempTimes = []
    tempKeys = []
    for i in range(len(times)):
        if(times[i]<time):
            if(times[i]>time-secs_till_delete):
                tempTimes.append(times[i])
                tempKeys.append(ascii[i])
    return tempTimes,tempKeys

#===============================================================================
#generate the video
#===============================================================================
frameTime = 0
fig = 1
lastFig = round((times[-1] + secs_till_delete + 1)*FPS)
while(frameTime < times[-1] + secs_till_delete+1):
    plot_and_save(fig,frameTime)
    frameTime += FPS**-1
    fig += 1
    if fig%10==0:
        print "Fig " + str(fig) + " of " + str(lastFig) + " figs"

writer.release()
