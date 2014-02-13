#Class for sensors in birdbox
import spidev
import time

class adArray():
  def __init__(self):
    self.spi = spidev.SpiDev()
    self.spi.open(0,0)
    print "SPI Open"
  def spiGetValue(self,channel):
    if ((channel > 7) or (channel < 0)):
      return -1
 
    r = self.spi.xfer2([1,(8+channel)<<4,0])

    ret =  ((r[1]&3) << 8) + (r[2] >> 2)
    return ret
  def lightValue(self):
    return self.spiGetValue(0)

  def inIrValue(self):
    return self.spiGetValue(1)

  def outIrValue(self):
    return self.spiGetValue(2) 
  def tempValue(self):
    tfile = open("/sys/bus/w1/devices/28-000001a70d1f/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    tempData = secondline.split(" ")[9]
    temp =float(tempData[2:])
    temp = temp /1000
    return temp
