import sqlite3 as sql
from datetime import datetime

class datastore():
  def __init__(self,fileName):
    #Try to connect to database
    self.con = sql.connect(fileName)
    self.cur = self.con.cursor()
    self.cur.execute('SELECT SQLITE_VERSION()')
    data = self.cur.fetchone()
    print "Connected to database %s using sqlite version number %s" % (fileName,data[0])
  def createNewStore(self):
    self.cur.execute('CREATE TABLE LightTemp(id INT, datavalue FLOAT, datastamp TEXT)')
    self.cur.execute('CREATE TABLE Door(id INT, inout TEXT, datestamp TEXT)')

  def registerExit(self):
    timestamp = str(datetime.now())
    sqlQuery = "INSERT INTO Door VALUES (1,'exit','" + timestamp + "')"
    self.cur.execute(sqlQuery)
    self.con.commit()
  def registerEntry(self):   
    timestamp = str(datetime.now())
    sqlQuery = "INSERT INTO Door VALUES (2,'entry','" + timestamp + "')"
    self.cur.execute(sqlQuery)
    self.con.commit()
  def registerLight(self, value):
    timestamp = str(datetime.now())
    sqlQuery = "INSERT INTO LightTemp VALUES (3," + str(value) + ",'" + timestamp + "')"
    self.cur.execute(sqlQuery)
    self.con.commit()
  def registerTemp(self,value):
    timestamp = str(datetime.now())
    sqlQuery = "INSERT INTO LightTemp VALUES (4," + str(value) + ",'" + timestamp + "')"
    self.cur.execute(sqlQuery)
    self.con.commit()

