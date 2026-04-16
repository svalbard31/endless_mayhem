from math import cos, sin
gravtiy = 10 
angle = 0
pos = [0,0]
speed = [0,0]
acceleration = [0,0]
borders = [1000,1000]
thrustscalar = 20

def thrust():
    thrustx = 20*cos(angle)
    thrusty = 20*sin(angle)
    acceleration[0]+= thrustx
    acceleration[1]+= thrusty 
def gravity():
    acceleration[1] -=10

def turnleft(): 
    global angle
    angle+=3 
    if angle>360:
        diff = angle - 360
        angle = 0 +diff
def turnrigt():
    global angle
    angle-=3 
    if angle<0:
        angle = 360 - angle 


def clamp(): #This is in practice collision detection 
    if pos[0]<= 0: 
        pos[0] = 0
        if speed[0]<= 0:
            speed[0] = 0
        if acceleration[0]<=0:
            acceleration[0] = 0
    if pos[0]>= 1000: 
        pos[0] = 1000
        if speed[0]>= 0:
            speed[0] = 0
        if acceleration[0]>=0:
            acceleration[0] = 0
    if pos[1]<= 0: 
        pos[1] = 0
        if speed[1]<= 0:
            speed[1] = 0
        if acceleration[1]<=0:
            acceleration[1] = 0
    if pos[1]>= 1000: 
        pos[1] = 1000
        if speed[1]>= 0:
            speed[1] = 0
        if acceleration[1]>=0:
            acceleration[1] = 0


    

        

    
