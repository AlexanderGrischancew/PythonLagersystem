#Autor: Alexander Grischancew
#Name:  datenbankAPI.py
#Zweck: nimmt die Daten von funktionen.py entgegen und verartbeitet die Komunikation zwsichen Python und MySQL

#-IMPORTS----------
from dbStart import *

try:
    import pymysql as mdb
except:
    import MySQLdb as mdb
#------------------


#-SETUP------------

#--DB_SETUP--------
dbCon = dbStart()
dbCur = dbCon.cursor()
#------------------
#------------------

#-FUNCTIONS--------
def DBcreateItem(name,description,storageName,shelfNumber,partitionNumber,amount,autoOrder = 0):
    with dbCon:
        #-insert-block---
        dbCur.execute("INSERT INTO Items(Name,Description,Amount,AutoOrder) VALUES('%s','%s','%s','%s')" % (name,description,amount,autoOrder)) #insert
        #----------------
        #-get-block------
        dbCur.execute("SELECT ItemID FROM Items where name = '%s'"                      % (name))           #getItemID
        itemID      = dbCur.fetchone()
        dbCur.execute("SELECT StorageID FROM Storages where name = '%s'"                % (storageName))    #getStorageID
        storageID   = dbCur.fetchone()
        dbCur.execute("SELECT ShelfID FROM Shelves where ShelfNumber = '%s'"            % (shelfNumber))    #getShelfID
        shelfID     = dbCur.fetchone()
        dbCur.execute("SELECT PartitionID FROM Partitions where PartitionNumber = '%s'" % (partitionNumber))#getPartitionID
        partitionID = dbCur.fetchone()
        #----------------
        #-insert-block---
        dbCur.execute("INSERT INTO Locations(ItemID,StorageID,ShelfID,PartitionID) VALUES('%s','%s','%s','%s')" % (itemID[0],storageID[0],shelfID[0],partitionID[0]))    #insert
        #----------------
        
def DBcreateStorage(storageName,description):
    with dbCon:
        #-insert-block---
        dbCur.execute("INSERT INTO storages(Name,Description) VALUES('%s','%s')" % (storageName,description))   #insert
        #----------------
        
def DBcreateShelf(shelfNumber,storageName):
    with dbCon:
        #-insert-block---
        dbCur.execute("INSERT INTO shelves(ShelfNumber) VALUES('%s')"       % (shelfNumber))    #insert
        #----------------
        #-get-block------
        dbCur.execute("SELECT StorageID FROM Storages where Name = '%s'"    % (storageName))    #getStorageID
        storageID = dbCur.fetchone()
        dbCur.execute("SELECT ShelfID FROM Shelves where ShelfNumber = '%s'"% (shelfNumber))    #getShelfID
        shelfID = dbCur.fetchone()
        #----------------
        #-insert-block---
        dbCur.execute("INSERT INTO ShelfLocations(StorageID,ShelfID) VALUES('%s','%s')" % (storageID[0],shelfID[0]))  #insert
        #----------------
        
def DBcreatePartition(partitionNumber,shelfNumber):
    with dbCon:
        #-insert-block---
        dbCur.execute("INSERT INTO Partitions(PartitionNumber) VALUES('%s')"            % (partitionNumber))    #insert
        #----------------
        #-get-block------
        dbCur.execute("SELECT PartitionID FROM Partitions where PartitionNumber = '%s'" % (partitionNumber))    #getPartitionID
        partitionID = dbCur.fetchone()
        dbCur.execute("SELECT ShelfID FROM Shelves where ShelfNumber = '%s'"            % (shelfNumber))        #getShelfID
        shelfID = dbCur.fetchone()
        #----------------
        #-insert-block---
        dbCur.execute("INSERT INTO PartitionLocations(PartitionID,ShelfID) VALUES('%s','%s')"   % (partitionID[0],shelfID[0])) #insert
        #----------------
        
def DBupdateItem(name,description = "",storageName = "",shelfNumber = "",partitionNumber = "",autoOrder = "",amount= ""):
    with dbCon:
        dbCur.execute("SELECT ItemID FROM Items where name = '%s'"  % (name)) #getItemID
        itemID      = dbCur.fetchone()

        if description != "":
            dbCur.execute("UPDATE Items SET Description = '%s' where ItemID = '%s'" % (description,itemID[0]))       #update
        if amount != "":
            dbCur.execute("UPDATE Items SET amount = '%s' where ItemID = '%s'"% (amount,itemID[0]))       #update
        if autoOrder != "":
            dbCur.execute("UPDATE Items SET AutoOrder = '%s' where ItemID = '%s'"% (autoOrder,itemID[0])) #update

            
        if storageName != "":
            dbCur.execute("SELECT StorageID FROM Storages where name = '%s'"                % (storageName))                #getStorageID
            storageID   = dbCur.fetchone()
        
            dbCur.execute("UPDATE Locations SET StorageID = '%s' where ItemID = '%s'"         % (storageID[0],itemID[0]))     #update
                
        if shelfNumber != "":
            dbCur.execute("SELECT ShelfID FROM Shelves where ShelfNumber = '%s'"            % (shelfNumber))                #getShelfID
            shelfID     = dbCur.fetchone()

            dbCur.execute("UPDATE Locations SET ShelfID = '%s' where ItemID = '%s'"           % (shelfID[0],itemID[0]))       #update
                
        if partitionNumber != "":
            dbCur.execute("SELECT PartitionID FROM Partitions where PartitionNumber = '%s'" % (partitionNumber))            #getPartitionID
            partitionID = dbCur.fetchone()
        
            dbCur.execute("UPDATE Locations SET PartitionID = '%s' where ItemID = '%s'"       % (partitionID[0],itemID[0]))   #update

def DBdeleteItem(name):
    with dbCon:
        dbCur.execute("DELETE FROM Items WHERE Name = '%s'" % (name))

def DBsearchItem(name):
    with dbCon:
        #dbCur.execute("SELECT Name, Description FROM Items WHERE MATCH (Name) AGAINST ('%s' IN NATURAL LANGUAGE MODE)" % (name))# THIS SHIT DOESN'T WORK!
        dbCur.execute("SELECT Name, Description FROM Items WHERE Name LIKE '%s' " % (name))
        searchResults = list(dbCur.fetchall())
        return searchResults
        
        
def DBselectItem(item = "all"):
    with dbCon:
        if item == "all":
            itemParameters = []
            dbCur.execute("SELECT ItemID FROM Items ORDER BY name")
            results = list(dbCur.fetchall())
            for itemID in results:
                dbCur.execute("SELECT Name,Description,Amount,AutoOrder FROM Items WHERE ItemID = '%s'" % (itemID))
                parameterResults = list(dbCur.fetchone())
                dbCur.execute("SELECT StorageID,ShelfID,PartitionID FROM Locations WHERE ItemID = '%s'" % (itemID))
                locationResults = list(dbCur.fetchone())
                
                dbCur.execute("SELECT name FROM Storages where StorageID = '%s'"                % (locationResults[0]))    
                locationResults[0]   = dbCur.fetchone()[0]
                dbCur.execute("SELECT ShelfNumber FROM Shelves where ShelfID = '%s'"            % (locationResults[1]))    
                locationResults[1]  = dbCur.fetchone()[0]
                dbCur.execute("SELECT PartitionNumber FROM Partitions where  PartitionID = '%s'" % (locationResults[2]))
                locationResults[2] = dbCur.fetchone()[0]
                
                itemParameters.append([parameterResults,locationResults])
                          
        else:
            dbCur.execute("SELECT ItemID FROM Items where name = '%s'"    % (item))    #getItem Parameters
            try:
                itemID = dbCur.fetchone()[0]
            except:
                return
            dbCur.execute("SELECT Name,Description,Amount,AutoOrder FROM Items where name = '%s'"    % (item))    #getItem Parameters
            itemParameters = list(dbCur.fetchone())
            dbCur.execute("SELECT StorageID,ShelfID,PartitionID FROM Locations WHERE ItemID = '%s'" % (itemID))
            locationResults = list(dbCur.fetchone())

            dbCur.execute("SELECT name FROM Storages where StorageID = '%s'"                % (locationResults[0]))    
            locationResults[0]   = dbCur.fetchone()[0]
            dbCur.execute("SELECT ShelfNumber FROM Shelves where ShelfID = '%s'"            % (locationResults[1]))    
            locationResults[1]  = dbCur.fetchone()[0]
            dbCur.execute("SELECT PartitionNumber FROM Partitions where  PartitionID = '%s'" % (locationResults[2]))
            locationResults[2] = dbCur.fetchone()[0]
            
            itemParameters.append(locationResults)  
            
        return itemParameters

def DBselectShelve(name):
    with dbCon:
        dbCur.execute("SELECT ShelfID FROM Shelves WHERE ShelfNumber = '%s'"    % (name))    #getShelfID
        try:
            shelveID = dbCur.fetchone()[0]
        except: #if dbCur.fetchone() is empty 
            shelveParameters = "Für '"+ str(name) + "' wurde kein Regal gefunden"
            return shelveParameters
        dbCur.execute("SELECT StorageID FROM shelflocations WHERE ShelfID = '%s'"    % (shelveID))    #getStorageID
        storageID = dbCur.fetchone()[0]
        dbCur.execute("SELECT Name FROM storages WHERE storageID = '%s'"    % (storageID))    #getStorageID
        storage = list(dbCur.fetchone())
        return storage

def DBselectPartition(name):
    with dbCon:
        dbCur.execute("SELECT PartitionID FROM Partitions WHERE PartitionNumber = '%s'"    % (name))    #getPartitionID
        try:
            partitionID = dbCur.fetchone()[0]
        except: #if dbCur.fetchone() is empty 
            partitionParameters = "Für '"+ str(name) + "' wurde kein Abteil gefunden"
            return partitionParameters
        dbCur.execute("SELECT ShelfID FROM partitionlocations WHERE partitionID = '%s'"    % (partitionID))    #getStorageID
        shelfID = dbCur.fetchone()[0]
        dbCur.execute("SELECT ShelfNumber FROM Shelves WHERE ShelfID = '%s'"    % (shelfID))    #getStorageID
        shelf = list(dbCur.fetchone())
        return shelf

def DBselectStorage(name):#von DBselectAllStorage abgetrennt um die Ausmaße der Funktion zu verringern
    with dbCon:
        dbCur.execute("SELECT Name,Description FROM Storages WHERE Name = '%s'"    % (name))    #getStorageParameters
        try:
            storageParameters = list(dbCur.fetchone())
        except TypeError: #if dbCur.fetchone() is empty 
            storageParameters = "Für '"+ str(name) + "' wurde kein Lager gefunden"
        return storageParameters

        
def DBselectAllStorage():#(alex sein werk)
    with dbCon:
        #-SETUP-----------
        storages = []
        storagesBuffer = []
        allShelves = []
        shelvesBuffer = []
        allStorage = []
        allPartitions = []
        #-----------------

        #-GET_STORAGE---------------------------
        dbCur.execute("SELECT * FROM storages")
        storageResults = dbCur.fetchall()
        for row in storageResults:
            storages.append(row[0])
        #---------------------------------------
            
        #-GET_SHELVES_OF_STORAGES------------------------------------------------------------------
        for storage in storages:
            dbCur.execute("SELECT ShelfID FROM shelflocations WHERE StorageID ='%s'"%(storage))
            shelveResults = dbCur.fetchall()
            
            if len(shelveResults)==0:
                storagesBuffer.append([storage,[]])
            else:
                for row in shelveResults:
                    allShelves.append(row[0])
                storagesBuffer.append([storage,allShelves])
                allShelves = []
        #------------------------------------------------------------------------------------------

        #-GET_PARTITIONS_OF_SHELVES----------------------------------------------------------------------------------
        for storage in storagesBuffer:
            for shelveNr in storage[1]:
                dbCur.execute("SELECT PartitionID FROM partitionlocations WHERE shelfID ='%s' "%(shelveNr))
                partitions = dbCur.fetchall()
                for partition in partitions:
                    dbCur.execute("SELECT PartitionNumber FROM partitions WHERE PartitionID ='%s' "%(partition[0]))#Covert ID to name
                    partitionsNumbers = dbCur.fetchall()
                    allPartitions.append(partitionsNumbers[0][0])
                shelve = [shelveNr,allPartitions]
                shelvesBuffer.append(shelve)
                allPartitions = []
              
            allStorage.append([storage[0],shelvesBuffer])
            shelvesBuffer = []


        #-------------------------------------------------------------------------------------------------------------

        #-CONVERT_IDS_TO_NAMES---------------------------------------------------------------------------------------------
        
        for storage in allStorage:
            for shelf in storage:
                if type(shelf) != int:
                    try:
                        dbCur.execute("SELECT ShelfNumber FROM shelves WHERE ShelfID = '%s'" %(shelf[0][0]))
                        shelfNumber = dbCur.fetchone()
                        shelf[0][0] = shelfNumber[0]
                    except:
                        pass
  
            dbCur.execute("SELECT Name FROM storages WHERE StorageID ='%s' "%(storage[0]))
            storageName = dbCur.fetchone()
            storage[0] =  storageName[0]
        
        #------------------------------------------------------------------------------------------------------------------
                    
        
        return allStorage

def DBupdateStorage(name,description):
    with dbCon:
        dbCur.execute("SELECT StorageID FROM storages WHERE name = '%s'" %(name))
        storageID = dbCur.fetchone()[0]
        dbCur.execute("UPDATE storages SET Description = '%s' where StorageID = '%s'"% (description,storageID))     #update
                      
def DBupdateShelve(name,storageName):
    with dbCon:
        dbCur.execute("SELECT ShelfID FROM shelves WHERE ShelfNumber = '%s'" %(name))
        shelveID = dbCur.fetchone()[0]
        dbCur.execute("SELECT StorageID FROM storages WHERE name = '%s'" %(storageName))
        storageID = dbCur.fetchone()[0]
        dbCur.execute("UPDATE shelflocations SET storageID = '%s' where StorageID = '%s'"% (storageID,shelveID))     #update
        
def DBupdatePartition(name,shelveName):
    with dbCon:
        dbCur.execute("SELECT PartitionID FROM partitions WHERE PartitionNumber = '%s'" %(name))
        partitionID = dbCur.fetchone()[0]
        dbCur.execute("SELECT ShelfID FROM shelves WHERE ShelfNumber = '%s'" %(shelveName))
        shelveID = dbCur.fetchone()[0]
        dbCur.execute("UPDATE partitionlocations SET shelfID = '%s' where partitionID = '%s'"% (shelveID,partitionID))     #update
#------------------
