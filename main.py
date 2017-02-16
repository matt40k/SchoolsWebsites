#!/usr/bin/python
import sqlite3
import os
import urlparse
import csv
import sys
from urllib2 import urlopen
import json
import datetime
import tweepy
import ConfigParser

# Define variables
dbName	   = 'school.db'					# Defined the database filename
edubaseUrl = 'https://getedubaseurl.apphb.com/api/Product/'	# Url to the latest Edubase data extract URL
configFile = 'config.txt'

# Get timestamp
def now () :
	return datetime.datetime.now()

# Read file
def readFile ( fileName ) :
	with open(fileName, 'rb') as fileContent :
		return fileContent.read()

# Execute SQL script
def execSql ( cmd ) :
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	c.execute( cmd )
	result = c.fetchone()
	conn.commit()
	conn.close()
	return result

# Execute SQL script to insert into stagingEdubase
def execSqlInsertIntoStagingEdubase ( Urn, LaCode, LaName, EstablishmentCode, EstablishmentName, TypeOfEstablishment, SchoolWebsite, Domain, HeadName, HeadJobTitle ) :
	conn = sqlite3.connect(dbName)
	conn.text_factory = str
	c = conn.cursor()
	c.execute("INSERT or REPLACE INTO stagingEdubase (Urn, LaCode, LaName, EstablishmentCode, EstablishmentName, TypeOfEstablishment, SchoolWebsite, Domain, HeadName, HeadJobTitle) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(Urn, LaCode, LaName, EstablishmentCode, EstablishmentName, TypeOfEstablishment, SchoolWebsite, Domain, HeadName, HeadJobTitle))
	result = c.fetchone()
	conn.commit()
	conn.close()
	return result

# Delete old Edubase extracts
def delOldDumps ( ) :
        filelist = [ f for f in os.listdir(".") if f.endswith(".csv") ]
        for f in filelist:
                os.remove(f)
        return

# Downloads the latest Edubase data extract
def GetLatestEdubaseDump ( ) :
	response = urlopen(edubaseUrl)
	dumpUrl = json.loads(response.read())[0]["AllDownloadUrl"]
	dumpName = urlparse.urlsplit(dumpUrl).path.split('/')[-1]
	if ( not os.path.isfile(dumpName) ):
	        delOldDumps()
	        print ("Downloading Edubase data...")
	        f = urlopen(dumpUrl)
		dumpName = os.path.basename(dumpUrl)
		with open(dumpName, "wb") as local_file:
	            local_file.write(f.read())
		ClearStaging()
		ImportEdubaseDump(dumpName)		

# Create database
def CreateDatabase ( ) :
	if ( not os.path.exists(dbName) ) :
		print ("Creating database...")
		sqlFiles = os.listdir("sql")
		for sqlFile in sqlFiles :
			if (not sqlFile.startswith("merge_")) :
				print (" - Running SQL Script - " + sqlFile)
				cmdCreateTable = readFile("sql/" + sqlFile)
				execSql(cmdCreateTable)

# Insert record into Schools
def InsertSchool ( Urn, LaCode, LaName, EstablishmentCode, EstablishmentName, TypeOfEstablishment, SchoolWebsite, HeadJobTitle, HeadName ,ModifiedDateTime ) :
	LaName				= LaName.replace("'", "''")
	EstablishmentName		= EstablishmentName.replace("'", "''")
	TypeOfEstablishment		= TypeOfEstablishment.replace("'", "''")
	SchoolWebsite			= SchoolWebsite.replace("'", "''")
	HeadJobTitle			= HeadJobTitle.replace("'", "''")
	HeadName			= HeadName.replace("'", "''")	
	if ( not Urn or Urn.isspace() ) :
		Urn			= None
	if ( not LaCode or LaCode.isspace() ) :
		LaCode			= None
	if ( not EstablishmentCode or EstablishmentCode.isspace() ) :
		EstablishmentCode	= None
	
	#ModifiedDateTime		= str(ModifiedDateTime).replace("'", "''")
	Domain				= GetDomain(SchoolWebsite) 
	#IsSchUk			= GetIsSchUk(Domain)

	
	
	print ( " - Add School: " + Urn ) # + " - " + str(IsSchUk))
	execSqlInsertIntoStagingEdubase(Urn, LaCode, LaName, EstablishmentCode, EstablishmentName, TypeOfEstablishment, SchoolWebsite, Domain, HeadName, HeadJobTitle)

# Gets the domain name from the Url
def GetDomain ( url ) :
        url = url.replace('https://', '').replace('http://', '').replace('www.', '') + '/'
        url = url[0:url.index('/')]
        return;

# Is the domain name a .sch.uk domain?
def GetIsSchUk ( domain ) :
	if ( domain == None) :	
		return False;
	if ( len(domain) < 8 ) :
		return False;
	if ( domain[-7:] == '.sch.uk' ) :
		return True;
	else :
		return False;

# Use the Mythic-Beasts IPv6 health check to get IPv6 score (out of 10)
def GetIPv6Result ( domain ) :
        ip6HealthCheck = "https://www.mythic-beasts.com/ipv6/health-check?domain=" + domain + "&json=1&submit="
        response = urlopen(ip6HealthCheck)
        respJson = json.loads(response.read())
        noResults = len(respJson)
        c = 0
        score = 0
        while c < noResults:
                print respJson[c]["name"] + "=" + respJson[c]["result"]
                if (respJson[c]["result"] == "PASS"):
                        score += 1
                c += 1
	#       print respJson[key]["name"] + " - " + respJson[key]["result"]
	return score

# Print a line to the console.
def PrintLine ( ) :
	print ("======================================")

# Post a Tweet to Twitter.
def Tweet ( tweetMessage ) :
	consumer_key		= GetFileConfig('Twitter', 'consumer_key')
	consumer_secret		= GetFileConfig('Twitter', 'consumer_secret')
	access_token		= GetFileConfig('Twitter', 'access_token')
	access_token_secret	= GetFileConfig('Twitter', 'access_token_secret')
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	api.update_status(status=tweetMessage)

# Import the Edubase csv file into the database.
def ImportEdubaseDump ( eduBaseFileName ) :
	rowNo = 0
	with open(eduBaseFileName) as csvfile :
        	reader = csv.DictReader(csvfile)
        	for row in reader :
			if (rowNo > 0) :
				Urn = row["URN"]
				LaCode = row["LA (code)"]
				LaName = row["LA (name)"]
				EstablishmentCode = row["EstablishmentNumber"]
				EstablishmentName = row["EstablishmentName"]
				TypeOfEstablishment = row["TypeOfEstablishment (name)"]
				SchoolWebsite = row["SchoolWebsite"]
				HeadJobTitle = row["HeadPreferredJobTitle"]
				space = " "
				HeadTitle = str(row["HeadTitle (name)"])
				HeadFirstName = str(row["HeadFirstName"])
				HeadLastName = str(row["HeadLastName"])
				HeadName = HeadTitle + space + HeadFirstName + space + HeadLastName
				HeadName = HeadName.replace("  ", "")
			
				InsertSchool(Urn, LaCode, LaName, EstablishmentCode, EstablishmentName, TypeOfEstablishment, SchoolWebsite, HeadJobTitle, HeadName, now() )

               		rowNo += 1
################
# Configuration
################
# Read config from database
def GetConfig ( ConfigItem ) : 
	configSql = ("SELECT Value FROM config where Name = '" + ConfigItem + "'")
	configVal = execSql(configSql)
	return configVal
# Set config to database
def SetConfig ( ConfigItem, ConfigType ) :
	configSql = ("INSERT or REPLACE INTO config (Name, Value) VALUES ('" + ConfigItem + "', '" + ConfigValue + "'")
	execSql(configSql)
# Read config from file
def GetFileConfig ( ConfigSection, ConfigItem ) :
	cfg = ConfigParser.RawConfigParser()
	cfg.read(configFile)
	ConfigValue = cfg.get(ConfigSection, ConfigItem)
	return ConfigValue
# Set config to database	
def SetFileConfig ( ConfigSection, ConfigItem, ConfigValue ) :
	cfg = ConfigParser.RawConfigParser()
	cfg.add_section(ConfigSection)
	config.set(ConfigSection, ConfigItem, ConfigValue)
	with open(configFile, 'wb') as configfile :
		cfg.write(configfile)
		
################
# Cleaning		
################		
# Delete database and remove any csv files.
def ClearDown ( ) :
	delOldDumps()
	if ( os.path.isfile(dbName) ) :
		os.remove(dbName)	

# Clear down the Staging table - stagingEdubase
def ClearStaging ( ) :
	execSql( "DELETE FROM stagingEdubase;" )
	execSql( "VACUUM;" )
	
######################

print ( "Start  = %s" % now() ) 
PrintLine()

#ClearDown()
CreateDatabase()
GetLatestEdubaseDump()
sqlOut = readFile("sql/merge_stagingEdubase_to_school.sql")
output1 = execSql(sqlOut)
noOfSchools = execSql("select count(1) from school_detail;")
print noOfSchools

PrintLine()
print ( "Finish = %s" % now() )
