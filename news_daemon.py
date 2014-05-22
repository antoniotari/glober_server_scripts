#!/usr/bin/python
import time
from daemon import runner
import MySQLdb
import json
import urllib2
import base64
#from defs import *


ESPN_APIKEY=    'ufuancvzf7xb58f9zh7khr32'
ESPN_BASEURL=   'http://api.espn.com/v1/'

class App():
        def __init__(self):
                self.stdin_path = '/dev/null'
                self.stdout_path = '/dev/tty'
                self.stderr_path = '/dev/tty'
                self.pidfile_path =  '/tmp/foo3.pid'
                self.pidfile_timeout = 5

        def run(self):
                while True:
                        #self.EraseWaitingPicChat()
                        #time.sleep(11)
                        #self.EraseActiveUser()
                        #f=open('/var/www/sportapp/teamnews.txt','w')
                        #f.write("")
                        #f.close()
                        self.SaveSportNews()
                        time.sleep(60*60*4)

	def ClearFile(self):
		f=open('/var/www/sportapp/teamnews.txt','w')
                f.write("")
                f.close()		

	def GetAllNews(self,sport):
		baseballD={}
		try:
                        baseballJ=urllib2.urlopen(ESPN_BASEURL+"sports/%s/news/headlines/?apikey=%s"%(sport,ESPN_APIKEY)).read()
                        baseballD = json.loads(u''+baseballJ)
                        baseballA = baseballD['headlines']
                        resultCount=baseballD['resultsCount']
                        counter=baseballD['resultsOffset']
                        limit=baseballD['resultsLimit']
                        counter=counter+limit
			if resultCount>40:resultCount=40
                        while(counter<resultCount):
                        	time.sleep(3)
			        baseballJ=urllib2.urlopen(ESPN_BASEURL+"sports/%s/news?apikey=%s&offset=%d"%(sport,ESPN_APIKEY,counter)).read()
                                baseballA2 = json.loads(u''+baseballJ)['headlines']
                                for row in baseballA2:
                                        baseballA.append(row)
                                counter=counter+limit
                	time.sleep(3)
                except:
                        baseballD={}
		baseballD['headlines']=baseballA
		baseballD['totalcount']=len(baseballA)
		return baseballD

        #get the news for all the sports
        def SaveSportNews(self):
                #BASEBALL
		#baseballJ=urllib2.urlopen(ESPN_BASEURL+"sports/baseball/news?apikey="+ESPN_APIKEY).read()
                #baseballD = json.loads(u''+baseballJ)
		baseballJ=json.dumps(self.GetAllNews('baseball'))
		#HOCKEY
		hockeyJ=json.dumps(self.GetAllNews('hockey'))
		#hockeyJ=urllib2.urlopen(ESPN_BASEURL+"sports/hockey/news?apikey="+ESPN_APIKEY).read()
		#time.sleep(2)
                #SOCCER
                soccerJ=json.dumps(self.GetAllNews('soccer'))
		#soccerJ=urllib2.urlopen(ESPN_BASEURL+"sports/soccer/news?apikey="+ESPN_APIKEY).read()
                #FOOTBALL
                #footballJ=urllib2.urlopen(ESPN_BASEURL+"sports/football/news?apikey="+ESPN_APIKEY).read()
                #time.sleep(2)
		footballJ=json.dumps(self.GetAllNews('football'))
                #BASKETBALL
                #basketballJ=urllib2.urlopen(ESPN_BASEURL+"sports/basketball/news?apikey="+ESPN_APIKEY).read()
		basketballJ=json.dumps(self.GetAllNews('basketball'))
                self.ClearFile()
		time.sleep(2)
		f=open('/var/www/sportapp/teamnews.txt','a')
                f.write("{\"result\":[%s,%s,%s,%s,%s],\"esit\":0}"%(baseballJ,hockeyJ,soccerJ,footballJ,basketballJ))
                f.close()

        def EraseWaitingPicChat(self):
                db=MySQLdb.connect(HOST,DBUSER,DBPASS,DBNAME)
                cursor=db.cursor(MySQLdb.cursors.DictCursor)
                sql="UPDATE ChatLog SET Message='' WHERE SendTime<(NOW()-INTERVAL 2 MINUTE) AND Message='afsjktirntly845kfhtk594jrtjh49lrtj4955555555klrktlrjkkjhhjkhgjhcom.antoniotari.glober.waiting_image';"
                try:
                        cursor.execute(sql)
                        db.commit()
                except:
                        db.rollback()
                finally:
                        cursor.close()
                        db.close()

        def EraseActiveUser(self):
                db=MySQLdb.connect(HOST,DBUSER,DBPASS,DBNAME)
                cursor=db.cursor(MySQLdb.cursors.DictCursor)
                sql="DELETE FROM ActiveUser WHERE LastPing<(NOW()-INTERVAL 5 MINUTE);"
                try:
                        cursor.execute(sql)
                        db.commit()
                except:
                        db.rollback()
                finally:
                        cursor.close()
                        db.close()

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

#Note that you'll need the python-deaemon library. In Ubuntu, you would:
#sudo apt-get install python-daemon
#Then just start it with ./howdy.py start, and stop it with ./howdy.py stop.                                                              
