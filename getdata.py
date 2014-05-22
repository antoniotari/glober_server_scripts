#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import json
import urllib2
import base64
import random
import string
import codecs
import sys

HOST=           'localhost'
DBUSER=         'antonio'
DBPASS=         'glorious.and.free'
DBNAME=         'teams'

ESPN_APIKEY=	'ufuancvzf7xb58f9zh7khr32'
ESPN_BASEURL=	'http://api.espn.com/v1/'

def validateValue(thedict,thekey):
	try:
		vaslue=thedict[thekey]
		try:
        		vaslueuni=unicode(vaslue, 'utf-8')
			return vaslueuni.replace("'","`").strip()
    		except TypeError:
        		#print 'error unicode validate'
			return vaslue.replace("'","`").strip()
	except:
		return ''

#db=MySQLdb.connect(HOST,DBUSER,DBPASS,DBNAME)
db = MySQLdb.connect(host=HOST,user=DBUSER,passwd=DBPASS,db=DBNAME,charset='utf8',use_unicode=True)
leaguesJ=urllib2.urlopen(ESPN_BASEURL+"sports/?apikey="+ESPN_APIKEY).read()
leaguesD = json.loads(u''+leaguesJ)
i=0
leagueGeneric2=leaguesD['sports']
for leagueGeneric in leagueGeneric2:
	j=0
	#leagueGeneric=leaguesD['sports'][i]
	#all leagues should have generic values of the sport
	try:
		sportName=validateValue(leagueGeneric,'name')
	except:
		sportName=''
	try:
		espn_sportId="%d"% leagueGeneric['id']
	except:
		espn_sportUid=''
	try:
		espn_sportUid= leagueGeneric['uid']
	except:
		espn_sportUid=''
	try:
		sport_links=json.dumps(leagueGeneric['links']['api'])
	except:
		sport_links=''
	#now parse the array of all the leagues for that sport
        try:
		leaguesA=leagueGeneric['leagues']
	except:
		leaguesA=[]
	for row in leaguesA:
        	#leaguesA=leagueGeneric['leagues']
		leagueName=validateValue(row,'name')
		try:
			leagueId="%d"%row['id']
		except:
			leagueId=''
		leagueUid=validateValue(row,'uid')
		try:
			leagueGroupid="%d"%row['groupId']
		except:
			leagueGroupid=''
		leagueAbbreviation=validateValue(row,'abbreviation')
		leagueShortName=validateValue(row,'shortName')
		#insert into database
		cursor=db.cursor(MySQLdb.cursors.DictCursor)
        	sql="INSERT INTO league (name,description,logo,sport,abbreviation,espn_id,espn_uid,espn_groupId,shortName,apilink,espn_sport_id,espn_sport_uid) VALUES ('"+"%s"%leagueName+"','','','"+sportName+unichr(300)+"','"+leagueAbbreviation+"','"+leagueId+"','"+leagueUid+"','"+leagueGroupid+"','"+"%s"%leagueShortName+"','"+sport_links+"','"+espn_sportId+"','"+espn_sportUid  +"');"
                try:
                        queryS=unicode(sql, 'utf-8')
                except TypeError:
                      	queryS=sql
			#print 'error unicode'
		
		try:
        		cursor.execute(queryS)
        		db.commit()
              	except:
			print 'commit exception'
        		db.rollback()
        	finally:
            		cursor.close()
		#print sportName+"\n"+espn_sportId+"\n"+espn_sportUid+"\n"+leagueAbbreviation+"\n"+sport_links+"\n"+leagueName+"\n"+leagueId+"\n"+leagueUid+"\n"+leagueGroupid

db.close()
