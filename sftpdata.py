import paramiko
import os
class sftpData():
  def __init__(self):
    print "SFTPing..."
  def send(self):
    DIR = '/home/pi/birdbox'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('hostname',port=22,username='*****',password='*****')
    sftp = ssh.open_sftp()
    print "sending database file"
    sftp.put(DIR + '/birdbox.db','birddata/birdbox.db')    
    for fname in os.listdir(DIR + '/images'):
      print "sending image file:" + fname
      sftp.put(DIR + '/images/' + fname, 'birddata/' + fname)
      print "removing local copy"
      os.remove(DIR + '/images/' + fname)
    sftp.close() 
        
