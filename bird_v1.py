#Main program code
import threading
import sensors
import datastore
import picamera
import sftpdata
import tweeter
import subprocess
import os
from time import sleep
from datetime import datetime
boxSensors = sensors.adArray()

event = 0
dataLight = 0
dataTemp = 0
threadRun = True
threadCount = 0
def mainThread():
  global event
  global dataLight
  global dataTemp
  global threadRun
  global threadCount
  print "Main thread starting..."
  subprocess.call(['modprobe','w1-gpio'])
  subprocess.call(['modprobe','w1-therm'])
  threadCount = threadCount + 1
  boxStore = datastore.datastore('./birdbox.db')
  if os.path.isfile('./birdbox.db'):
    print "Have database file using it..."
  else:
    #Create new table structure in above database   
    boxStore.createNewStore()

  while threadRun:
    if (event == 1):
      print "Store entry"
      boxStore.registerEntry()
      event = 0
      #tweet activity
      twt = tweeter.tweetit()
      print "Send Entry Tweet"
      twt.door("Entry")

    if (event == 2):
     print "Store exit"
     boxStore.registerExit()
     event = 0
     #tweet activity
     twt = tweeter.tweetit()
     print "Send Exit tweet"
     twt.door("Exit")
    if (event == 3):
      print "Store light value:" + str(dataLight)
      boxStore.registerLight(dataLight)
      event = 0
    if (event == 4):
      print "Store temp value:" + str(dataTemp)
      boxStore.registerTemp(dataTemp)
      event = 0
  threadCount = threadCount - 1
  

def twitter():
  global dataLight
  global dataTemp
  global threadRun
  global threadCount
  threadCount = threadCount + 1
  while threadRun:
    print "Sending tweet"
    twt = tweeter.tweetit()
    twt.send(dataTemp,dataLight)
    sleep(3600)
  threadCount = threadCount - 1

def readDoor():
  print "Door thread starting..."
  global event
  global threadRun
  global threadCount
  threadCount = threadCount + 1
  while threadRun:
    
    if (boxSensors.inIrValue() < 700):
      print "Bird Entry"
      event = 1

    if (boxSensors.outIrValue() < 700):
      print "Bird Exit"
      event = 2
    sleep(0.5)
  threadCount = threadCount - 1
def readEnv():
  print "Enviroment sensors thread starting..."
  global event
  global dataLight
  global dataTemp
  global threadRun
  global threadCount
  threadCount = threadCount + 1
  while threadRun:
    dataLight = boxSensors.lightValue()
    event = 3
    sleep(10)
    dataTemp = boxSensors.tempValue()
    event = 4
    sleep(600)
  threadCount = threadCount - 1

def takePicture():
  global threadRun
  global threadCount
  global dataLight
  print "Starting camera thread..."
  threadCount = threadCount + 1
  twPhoto = 11 #send a photo on start up
  while threadRun:
    timestamp = str(datetime.now())
    with picamera.PiCamera() as camera:
      camera.resolution = (640,480)
      camera.start_preview()
      sleep(2)
      camera.capture("images/" + timestamp + ".jpg")
      sleep(10)
      twPhoto = twPhoto + 1
      if twPhoto > 10:
        #send image to twitter not every time :-)
        if dataLight < 100:
          #only send if light ;-)
          twt = tweeter.tweetit()
          twt.photo("images/" + timestamp + ".jpg")
        twPhoto = 0
    sleep(600)
  threadCount = threadCount - 1

def sendData():
  global threadRun
  global threadCount
  threadCount = threadCount + 1
  print "Starting send data thread..."
  sender = sftpdata.sftpData()
  i = 0
  while threadRun:
    sleep(60)
    print "Send data at count:" + str(i) + " of 60"
    i = i + 1
    if i > 60:
      sender.send()
      i = 0
  threadCount = threadCount - 1    
    
    
t1 = threading.Thread(target=readDoor)
t1.start()

t2 = threading.Thread(target=mainThread)
t2.start()

t3 = threading.Thread(target=readEnv)
t3.start()

t4 = threading.Thread(target=takePicture)
t4.start()

t5 = threading.Thread(target=sendData)
t5.start()

t6 = threading.Thread(target=twitter)
t6.start()
try:
  while True:
    pass # do the loop here
except KeyboardInterrupt:
  threadRun = False
  while threadCount > 0:
    print "Waiting for " + str(threadCount) + " threads to stop..."
    sleep(20)
  print "All Done!"  
  
