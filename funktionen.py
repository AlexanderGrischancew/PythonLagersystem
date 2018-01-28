#Autor: Alexander Grischancew
#Name:  funktionen.py
#Zweck: Schleift Datenbank API befehle durch.


#-IMPORTS----------
from datenbankAPI import *
#------------------


#-SETUP------------
#------------------



#-FUNCTIONS--------
#Name:      createItem()
#Zweck:     leitet die Paramter vom GUI and die DBAPI weiter
#Parameter: nameEntry,descriptionEntry,storageNameEntry,shelfNameEntry,partitionNameEntry,autoOrderTickbox,amountEntry ALL AS CLASS OR STRING
#Return:    NONE IF SUCSSESFUL ELSE: STR: "---<ERROR>---"
def createItem(nameEntry,descriptionEntry,storageNameEntry,shelfNameEntry,partitionNameEntry,autoOrderTickbox,amountEntry):
    if type(nameEntry) ==  str:
        name            = nameEntry
    else:
        try:
            name = nameEntry.get()
        except:
            name = nameEntry["text"]
            
    if type(descriptionEntry) != str:
        description     = descriptionEntry.get()
    else:
        description     = descriptionEntry
        
    if type(storageNameEntry) != str:
        storageName     = storageNameEntry.get()
    else:
        storageName     = storageNameEntry
        
    if type(shelfNameEntry) != str:
        shelfName       = shelfNameEntry.get()
    else:
        shelfName       = shelfNameEntry
        
    if type(partitionNameEntry) != str:
        partitionName   = partitionNameEntry.get()
    else:
        partitionName   = partitionNameEntry
        
    if autoOrderTickbox != "1" and autoOrderTickbox != "0":
        autoOrder       = autoOrderTickbox.get()
        
    if type(amountEntry) != str:
        amount          = amountEntry.get()
    else:
        amount          = amountEntry
    #---------------------------------------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Es wurde kein Name eingegeben"
    elif storageName == "":
        message = "Es wurde kein Lager ausgewählt"
    elif shelfName == "":
        message = "Es wurde kein Regal ausgewählt"
    elif amount == "":
        message = "Es wurde keine Anzahl angegeben"
    #---------------------------------------------    
    else:
        message = DBcreateItem(name,description,storageName,shelfName,partitionName,amount,autoOrder)
    return message

#Name:      createStorage()
#Zweck:     leitet die Paramter vom GUI and die DBAPI weiter
#Parameter: nameEntry,descriptionEntry ALL AS CLASS OR STRING
#Return:    NONE IF SUCSSESFUL ELSE: STR: "---<ERROR>---"
def createStorage(nameEntry,descriptionEntry):
    #-get-block------------------------------------
    if type(nameEntry) != str:
        name            = nameEntry.get()
    else:
        name            = nameEntry
    if type(descriptionEntry) != str:
        description     =  descriptionEntry.get()
    else:
        description     =  descriptionEntry
    #---------------------------------------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Es wurde kein Name angegeben"
    #---------------------------------------------
    else:
        message = DBcreateStorage(name,description)
    return message

#Name:      createShelf()
#Zweck:     leitet die Paramter vom GUI and die DBAPI weiter
#Parameter: nameEntry,storageNameEntry ALL AS CLASS OR STRING
#Return:    NONE IF SUCSSESFUL ELSE: STR: "---<ERROR>---"
def createShelf(nameEntry,storageNameEntry):
    #-get-block-----------------------------------
    if type(nameEntry) != str:
        name            = nameEntry.get()
    else:
        name            = nameEntry
    if type(storageNameEntry) != str:
        storageName     = storageNameEntry.get()
    else:
        storageName     = storageNameEntry
    #---------------------------------------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Es wurde kein Name angegeben"
    elif storageName == "":
        message = "Es wurde kein Lager ausgewählt"
    #---------------------------------------------
    elif name != "" and storageName != "":
        message = DBcreateShelf(name,storageName)
    return message

#Name:      createPartition()
#Zweck:     leitet die Paramter vom GUI and die DBAPI weiter
#Parameter: nameEntry,shelfNameEntry ALL AS CLASS OR STRING
#Return:    NONE IF SUCSSESFUL ELSE: STR: "---<ERROR>---"
def createPartition(nameEntry,shelfNameEntry):
    #-get-block-----------------------------------
    if type(nameEntry) != str:
        name            = nameEntry.get()
    else:
        name            = nameEntry
    if type(shelfNameEntry) != str:
        shelfName  = shelfNameEntry.get()
    else:
        shelfName  = shelfNameEntry
    #---------------------------------------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Es wurde kein Name eingegeben"
    elif shelfName == "":
        message = "Es wurde kein Regal ausgewählt"
    #---------------------------------------------
    elif shelfName != "" and name != "":
        message = DBcreatePartition(name,shelfName)
    return message

#Name:      updateItem()
#Zweck:     leitet die Paramter vom GUI and die DBAPI weiter
#Parameter: nameEntry,descriptionEntry,storageNameEntry,shelfNameEntry,partitionNameEntry,autoOrderTickbox,amountEntry ALL AS CLASS OR STRING
#Return:    NONE IF SUCSSESFUL ELSE: STR: "---<ERROR>---"
def updateItem(nameEntry,descriptionEntry,storageNameEntry,shelfNameEntry,partitionNameEntry,autoOrderTickbox,amountEntry):
    #-get-block---------------------------------
    if type(nameEntry) ==  str:
        name            = nameEntry
    else:
        try:
            name = nameEntry.get()
        except:
            try:
                name = nameEntry["text"]
            except:
                name = ""
            
    if type(descriptionEntry) != str:
        description     = descriptionEntry.get()
    else:
        description     = descriptionEntry
        
    if type(storageNameEntry) != str:
        storageName     = storageNameEntry.get()
    else:
        storageName     = storageNameEntry
        
    if type(shelfNameEntry) != str:
        shelfName       = shelfNameEntry.get()
    else:
        shelfName       = shelfNameEntry
        
    if type(partitionNameEntry) != str:
        partitionName   = partitionNameEntry.get()
    else:
        partitionName   = partitionNameEntry
        
    if autoOrderTickbox != "1" and autoOrderTickbox != "0":
        autoOrder       = autoOrderTickbox.get()
        
    if type(amountEntry) != str:
        amount          = amountEntry.get()
    else:
        amount          = amountEntry
    #---------------------------------------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Es wurde kein Gegenstand ausgewählt"
    elif storageName == "":
        message = "Es wurde kein Lager ausgewählt"
    elif shelfName == "":
        message = "Es wurde kein Regal ausgewählt"
    elif amount == "":
        message = "Es wurde keine Anzahl angegeben"
    #---------------------------------------------    
    elif name != "" and storageName != "" and shelfName != "" and amount != "":
        message = DBupdateItem(name,description,storageName,shelfName,partitionName,autoOrder,amount)
    return message

#Name:      deleteItem(nameEntry)
#Zweck:     leitet die Paramter vom GUI and die DBAPI weiter
#Parameter: nameEntry (STRING OR CLASS)
#Return:    STR: "---<ERROR>---" if name == "" 
def deleteItem(nameEntry):
    if  type(nameEntry) != str:
        #get-block------
        name            = nameEntry.get()
        #---------------
    else:
        name = nameEntry
    #--messageBlock-------------------------------
    if name == "":
        message = "Gegenstand wurde nicht ausgewählt"
    #---------------------------------------------
    else:
        message = DBdeleteItem(name)
    return message

#Name:      searchItem()
#Zweck:     leitet die Parameter vom GUI and die DBAPI weiter
#Parameter: nameEntry (STRING OR CLASS)
#Return:    search Results vom MYsql AS ARRAY SORTED BY RELEVANCE [item,item2...]
def searchItem(nameEntry):
    #get-block-----
    if type(nameEntry) != str:
        name            = nameEntry.get()
    else:
        name = nameEntry
    #---------------
    clearName = name #coppy of name
    #--messageBlock-------------------------------
    if name == '':
        message = "Kein Gegendtand angegeben"
    #---------------------------------------------
    else:
        name = "%"+str(name)+"%" # so sql finds all results
        message = DBsearchItem(name)
    if message == []:
        message = "Für '"+clearName+"' wurde kein Gegenstand gefunden"
    return message

#Name:      selectItem()
#Zweck:     leitet die GUI parameter an DBAPI weiter
#Parameter: item (STRING OR CLASS) DEFAULT = "all"
#Return:    IF item = "all" all Items in DB (formatierung siehe Dokumentation) ELSE: Parameter of str(item) OR STR "---<ERROR>---" IF item NOT FOUND
def selectItem(item = "all"):
    if type(item) != str :
        #get-block------
        item = item.get()
        #---------------
    #--messageBlock-------------------------------
    if item == "":
        message = "Kein Gegendtand angegeben"
    #---------------------------------------------
    else:
        message = DBselectItem(item)
    if message == []:
        message = "Für '"+item+"' wurde kein Gegenstand gefunden"
    return message

#Name:      selectShelve
#Zweck:     leitet die Parameter an DBAPI weiter
#Parameter: name (STRING OR CLASS)
#Return:    [shelveName,storage] OR "---<ERROR>---" if shelve not found
def selectShelve(name):
    if type(name) != str:#die funktion wurde geschrieben dass sie mit typ: STR aufgerufen wird, sie kann jedoch mit typ: CLASS (TKINTER ENTRY) umgehen.
        #get-block-----
        name = name.get()
        #---------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Kein Regal angegeben"
    #---------------------------------------------
    else:
        message = DBselectShelve(name)
    if message == []:
        message = "Regal '"+name+"' wurde im System nicht gefunden"
    return message


#Name:      selectPartition
#Zweck:     leitet die Parameter an DBAPI weiter
#Parameter: name (STRING OR CLASS)
#Return:    [partitionName,shelve] OR "---<ERROR>---" if partition not found
def selectPartition(name):
    if type(name) != str:#die funktion wurde geschrieben dass sie mit typ: STR aufgerufen wird, sie kann jedoch mit typ: CLASS (TKINTER ENTRY) umgehen.
        #get-block-----
        name = name.get()
        #---------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Kein Abteil angegeben"
    #---------------------------------------------
    else:
        message = DBselectPartition(name)
    if message == []:
        message = "Abteil '"+name+"' wurde im System nicht gefunden"
    return message

#Name:      selectStorage
#Zweck:     leitet die Parameter an DBAPI weiter
#Parameter: name (STRING OR CLASS)
#Return:    [storageName,storageDescription] OR "---<ERROR>---" if storage not found
def selectStorage(name):#selectStorage wurde nicht wie bei Items mit selectAllStorage() vereint, weil die DBselectAllStorage() bereits zu viel code umfasst
    if type(name) != str:#die funktion wurde geschrieben dass sie mit typ: STR aufgerufen wird, sie kann jedoch mit typ: CLASS (TKINTER ENTRY) umgehen.
        #get-block-----
        name = name.get()
        #---------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Kein Lager angegeben"
    #---------------------------------------------
    else:
        message = DBselectStorage(name)
    if message == []:
        message = "Lager '"+name+"' wurde im System nicht gefunden"
    return message
    
#Name:      selectAllStorage()
#Zweck:     leitet die anfrage an die DBAPI weiter
#Parameter: NONE
#Return:    Lagersyetm: [[STORAGE[SHELVE[PARTITON1,PARTITION2][SHELVE2[PARTITION3]]...]...]...]
def selectAllStorage():
    message = DBselectAllStorage()
    return message

#Name:      updateStorage()
#Zweck:     Paramater von GUI an DBAPI weiterleiten   
#Parameter: nameEntry(STRING OR CLASS) descriptionEntry(STRING OR CLASS)
#Return:    NONE IF SUCCESFUL, STRING "--<ERROR>--" IF NOT SUCCESFULL
def updateStorage(nameEntry,descriptionEntry):
    #--getBlock-----------------------------------
    if type(nameEntry) != str:
        storage = nameEntry.get()
    if type(descriptionEntry) != str:
        description = descriptionEntry.get()
    #---------------------------------------------
    #--messageBlock-------------------------------
    if storage == "":
        message = "Kein Lager angegeben"
    #---------------------------------------------
    #--DBBlock------------------------------------
    else:
        message = DBupdateStorage(storage,description)
    #---------------------------------------------
    return message

#Name:      updateShelve()
#Zweck:     Paramater von GUI an DBAPI weiterleiten   
#Parameter: nameEntry(STRING OR CLASS) stroageNameEntry(STRING OR CLASS)
#Return:    NONE IF SUCCESFUL, STRING "--<ERROR>--" IF NOT SUCCESFULL
def updateShelve(nameEntry,storageNameEntry):
    #--getBlock------------------------------------
    if type(nameEntry) != str:
        name = nameEntry.get()
    else:
        name = nameEntry
    if type(storageNameEntry) != str:
        storageName = storageNameEntry.get()
    else:
        storageName = storageNameEntry
    #---------------------------------------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Kein Regal angegeben"
    elif storageName == "":
        message = "Kein Lager angegeben"
    #---------------------------------------------
    #--DBBlock------------------------------------
    elif name != "" and storageName != "":
        message = DBupdateShelve(name,storageName)
    #---------------------------------------------
    return message

#Name:      updatePartition()
#Zweck:     Paramater von GUI an DBAPI weiterleiten
#Parameter: nameEntry(STRING OR CLASS) shelveNameEntry(STRING OR CLASS)
#Return:    NONE IF SUCCESFUL, STRING "--<ERROR>--" IF NOT SUCCESFULL
def updatePartition(nameEntry,shelveNameEntry):
    #--getBlock-----------------------------------
    if type(nameEntry) != str:
        name = nameEntry.get()
    else:
        name = nameEntry
    if type(shelveNameEntry) != str:
        shelveName = shelveNameEntry.get()
    else:
        shelveName = shelveNameEntry
    #---------------------------------------------
    #--messageBlock-------------------------------
    if name == "":
        message = "Kein Abteil angegeben"
    elif shelveName == "":
        message = "Kein Regal angegeben"
    #---------------------------------------------
    #--DBBlock------------------------------------
    elif name != "" and shelveName != "":
        message = DBupdatePartition(name,shelveName)
    #---------------------------------------------
    return message
        




#------------------
