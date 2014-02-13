from twython import Twython
from datetime import datetime
CONSUMER_KEY = '****'
CONSUMER_SECRET = '******'
ACCESS_KEY = '*****'
ACCESS_SECRET = '********'
theTweet = 'My First Tweet'
class tweetit():
  def __init__(self):
    print "Tweeter Connect to twitter..."
    self.api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
  def send(self,temp,light):
    theTweet = "Birdbox temp:" + str(temp) + " light value:" + str(light) + " timestamp:" + str(datetime.now())
    self.api.update_status(status=theTweet)
  def door(self,status):
    theTweet = "Bird " + status + " detected at " + str(datetime.now())
    self.api.update_status(status=theTweet)
  def photo(self,aFilename):
    photo = open(aFilename,'rb')
    self.api.update_status_with_media(media=photo,status='Image')
