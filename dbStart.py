#Autor: Alexander Grischancew
#Name:  dbStart.py
#Zweck: Initialisiert die Komununikation zu der MySQL DB

#-IMPORTS----------
import pymysql as mdb
import configparser as confpras
import sys
#------------------

#-SETUP------------
#------------------



#-FUNCTIONS--------

#Name:      getConfig
#Zweck:     extrahiert die MySQL Zugangsdaten aus der DBconfigs.ini
#Parameter: NONE
#Return:    list(host,user,pw,DB) {all string}
def getConfig():
    config = confpras.ConfigParser()
    config.read("DBconfig.ini")
    
    user = config['MySQL']['Benutzer']
    DB = config['MySQL']['Datenbank']
    pw = config['MySQL']['Passwort']
    host = config['MySQL']['Host']

    DBacces = [host,user,pw,DB]
    return DBacces


#Name:      dbStart
#Zweck:     initialisiert die Verbindung mit der MySql Datanbank
#Parameter: NONE
#Return:    dbCon | class  OR error | str
def dbStart():
    DBacces = getConfig()

    
    try:
        dbCon = mdb.connect(DBacces[0],DBacces[1],DBacces[2],DBacces[3])
    except:
        print("Ein Fehler mit der Datenbak ist aufgetreten")
        sys.exit("Ein Fehler mit der Datenbak ist aufgetreten")
    

    return dbCon



#Name:      dbEnd
#Zweck:     Beendet die Verbindung zur MySQL DB
#Parameter: NONE
#Return:    NONE
def dbEnd(dbCon):
    dbCon.close()
    
#------------------
