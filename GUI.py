# GUI
# ProStorage System
# Made by:Alexander Grischancew
# Version 6.6.6

# --- Bibliotheken ---
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from funktionen import *
# --------------------

#---setup---
#-----------

# --- Funktionen ------------------------------------------------------------------

#---------------------functions going to DB----------------------------------------------------------------------------
def insertItem(createE2, createE3, createE4, createE5, createE6, cCB1, createSB1):
   message = createItem(createE2, createE3, createE4, createE5, createE6, cCB1, createSB1)#send to DB-API
   if type(message) == str:# when DB-API returns error report (type : STR)
      messagebox.showerror("Error",message)
   else:
      messagebox.showinfo("Erstellvorgang", "Gegenstand: '" + str(createE2.get())+"' wurde erfolgreich erstellt" )#own succes message
      clearCreateEntrys()
      refreshItemTreeview()

def GUIdeleteItem(nameEntry):
   if messagebox.askyesno("Löschen?", "Wollen Sie '"+str(nameEntry["text"])+"' wirklich löschen?"):#active opt-in (if user pushes "YES")
      name = nameEntry["text"]
      message = deleteItem(name) # going to DB
      if type(message) == str:# when DB-API returns error report (type : STR)
         messagebox.showerror("Error",message)
         return
      clearSearchResults()#Item doesnt exist now, clear the search results
      messagebox.showinfo("Löschvorgang", "Gegenstand: '"+str(nameEntry["text"])+"' wurde erfolgreich gelöscht" )#own succes message
      cancel()#delets all Entry windows
      search(searchE2)
      refreshItemTreeview()


def saveEdit(nameEntry,descriptionEntry,storageNameEntry,shelfNameEntry,partitionNameEntry,amountEntry,autoOrderTickbox):
   message = updateItem(nameEntry,descriptionEntry,storageNameEntry,shelfNameEntry,partitionNameEntry,autoOrderTickbox,amountEntry)
   if type(message) == str:# when DB-API returns error report (type : STR)
      messagebox.showerror("Error",message)
      return
   cancel()#delets all Entry windows
   search(searchE2)
   insertSearchItem(nameEntry["text"])#refreshes the search results as they are now changed in DB

def GUIselectStorage(nameEntry):
   clearStorageSearchEntrys()
   storage = selectStorage(nameEntry)
   if type(storage) == str:
      messagebox.showinfo("Suche",storage)
   else:
      storageNameEntryLabel["text"] = storage[0]
      storageDescriptionEntryLabel["text"] = storage[1]

def GUIselectShelve(nameEntry):
   clearShelveSearchEntrys()
   shelve = selectShelve(nameEntry)
   if type(shelve) == str:
      messagebox.showinfo("Suche",shelve)
   else:
      if type(nameEntry) == str:
         shelvesNameEntryLabel["text"] = nameEntry
      else:
         shelvesNameEntryLabel["text"] = nameEntry.get()
      shelvesDescriptionEntryLabel["text"] = shelve[0]

def GUIselectPartition(nameEntry):
   clearPartitionSearchEntrys()
   partition = selectPartition(nameEntry)
   if type(partition) == str:
      messagebox.showinfo("Suche",partition)
   else:
      if type(nameEntry) == str:
         partitionsNameEntryLabel["text"] = nameEntry
      else:
         partitionsNameEntryLabel["text"] = nameEntry.get()
      partitionsDescriptionEntryLabel["text"] = partition[0]

def saveStorageEdit(nameEntry,descriptionEntry):
   message = updateStorage(nameEntry,descriptionEntry)
   if type(message) == str:# when DB-API returns error report (type : STR)
      messagebox.showerror("Error",message)
      return
   cancelStorageEdit()
   GUIselectStorage(nameEntry)

def saveShelveEdit(nameEntry,storageEntry):
   message = updateShelve(nameEntry,storageEntry)
   if type(message) == str:# when DB-API returns error report (type : STR)
      messagebox.showerror("Error",message)
      return
   cancelShelveEdit()
   GUIselectShelve(nameEntry)

def savePartitionEdit(nameEntry,shelveEntry):
   message = updatePartition(nameEntry,shelveEntry)
   if type(message) == str:# when DB-API returns error report (type : STR)
      messagebox.showerror("Error",message)
      return
   cancelPartitionEdit()
   GUIselectPartition(nameEntry)

#---------------------------------------------------------------------------------------------------------------------

#----------------various clears/clean up commands-----------------------------------------------------
def clearStorageSearchEntrys():
   storageNameEntryLabel["text"] = ""
   storageDescriptionEntryLabel["text"] = ""

def clearShelveSearchEntrys():
   shelvesNameEntryLabel["text"] = ""
   shelvesDescriptionEntryLabel["text"] = ""

def clearPartitionSearchEntrys():
   partitionsNameEntryLabel["text"] = ""
   partitionsDescriptionEntryLabel["text"] = ""

def clearCreateEntrys():#mostly self explaning
   createE2.delete(0,END)
   createE3.delete(0,END)

   storageOptionsComboboxCreateItem.delete(0,END)
   shelveOptionsComboboxCreateItem.delete(0,END)
   partitionOptionsComboboxCreateItem.delete(0,END)

   createSB1.delete(0,END)
   createSB1.insert(0,"0")# insert value= "0" because an empty spinnbox eg. value = "" would cause issues if user trys to create item with amount "".

   createCB1.deselect()


def clearComboboxEntrys(ComboboxEntry1,ComboboxEntry2 = ""):# option to clean up one or two comboboxEntrys
   ComboboxEntry1.set("")# clean up first
   if ComboboxEntry2 != "":# check if there is a second one
      ComboboxEntry2.set("")# if there is, clean it up

def clearItemTreeview():
   for item in itemListTreeview.get_children():
    itemListTreeview.delete(item)

def clearStorageTreeview():
   for item in storageListTreeview.get_children():
    storageListTreeview.delete(item)
   #we don't need to delete the children, they get deleted with theier parent

def clearSearchResults():#self explaning
   searchL12["text"] = ""
   searchL13["text"] = ""
   searchL14["text"] = ""
   searchL15["text"] = ""
   searchL16["text"] = ""
   searchL17["text"] = ""
   searchL18["text"] = ""

#------------------------------------------------------------------------------------------------------

#--- various populate / refreh functions -------------------------------------------------------------

def populateStorageTreeview():
   storages = readStorage("storages")# get all Storages
   for storage in storages:#for every storage
      name = storage
      description = str(selectStorage(name)[1])# get description of storage (Return of function is: [storageName,Description])
      description = description.replace(" ","_")#Treeview doesn't like empty spaces while inserting, this converts all " " into "_" so that the whole text can be inserted
      storageListTreeview.insert('', 'end', name,text=name,values = "'"+description+"'")# insert storages with description into Treeview as Parent
      storageShelves = readStorage("shelves",name)#get shelves of storage
      for shelve in storageShelves:# for every shelve of storage
         shelveName = shelve
         storageListTreeview.insert(name, 'end',shelveName, text=shelveName,values = "Regal")#insert name into Treeview as child of storage
         partitionsInShelve = readStorage("partitions",str(shelveName))# get all partitions of shelve
         for partition in partitionsInShelve:#for every partition of the shelve
            partitionName = partition
            storageListTreeview.insert(shelveName, 'end', text=partitionName, values = "Abteil")#insert name as child of shelve (child of storage)


def populateItemTreeview():
   allItemsArray = selectItem("all")#get all Items

   for item in allItemsArray:# for every item
      lagerplatz = str(item[1][0])+" /"+str(item[1][1])+"/"+str(item[1][2]) # build a string that contains: storage name / shelve number / partition Number
      name = str(item[0][0]) # extract name
      anzahl = str(item[0][2]) #extract amount
      autoBestellung = str(item[0][3]) # extract bool auto order (1 or 0)

      #---Convert 0/1 to "yes"/"no"--
      if autoBestellung == "1":
         autoBestellung = "Ja"
      else:
         autoBestellung = "Nein"
      #------------------------------
      itemListTreeview.insert('', 'end', name,text=name,values = [lagerplatz,anzahl,autoBestellung] )#insert into treeview as parent

def refreshStorageTreeview():#self explaning
   clearStorageTreeview()
   populateStorageTreeview()

def refreshItemTreeview():#self explaning
   clearItemTreeview()
   populateItemTreeview()

#------------------------------------------------------------------------------------------------------

#------------------search functions-------------------------------------------------------------------

def searchResultTreeviewOnDoubleClick(usesles):# for some strange reason the binding gives a parameter, "useles" takes this argument and just keeps it
   item = searchResultsTreeview.selection()[0]
   insertSearchItem(item)

def itemListTreeviewOnDoubleClick(useles):# for some strange reason the binding gives a parameter, "useles" takes this argument and just keeps it
   item = itemListTreeview.selection()[0]
   search(item)
   tabs.select(searchF)

def storageListTreeviewOnDoubleClick(useles):
   item = storageListTreeview.selection()[0]
   values = storageListTreeview.set(item)

   if values["Beschreibung"] != "Regal" and values["Beschreibung"] != "Abteil" :
      tabs.select(manageStorage)
      searchStorageEntry.insert(0,item)
      GUIselectStorage(item)

   elif values["Beschreibung"] == "Regal":
      tabs.select(manageStorage)
      storageTabs.select(manageShelves)
      searchShelvesEntry.insert(0,item)
      GUIselectShelve(item)

   elif values["Beschreibung"] == "Abteil":
      print(item)
      tabs.select(manageStorage)
      storageTabs.select(managePartitions)
      searchPartitionsEntry.insert(0,item)
      GUIselectPartition(item)

def search(itemNameEntry):

   clearSearchResults()
   searchResult = searchItem(itemNameEntry)

   for item in searchResultsTreeview.get_children():#clear search results
    searchResultsTreeview.delete(item)

   if type(searchResult) == str:# when DB-API returns error report (type : STR)
      messagebox.showerror("Error",searchResult)
      return

   for item in searchResult:
      name = item[0]
      description = str(item[1]).replace(" ","_")
      searchResultsTreeview.insert('', 'end', name,text=name,values = "'"+description+"'")# insert storages with description into Treeview as Parent

   item = selectItem(itemNameEntry)#if db has a perfct 1:1 match...
   try:
      len(item)
   except:
      return
   insertSearchItem(item[0])#...insert it right away


def insertSearchItem(itemNameEntry):
   item = selectItem(itemNameEntry)
   if type(item) == str:# when DB-API returns error report (type : STR)
      messagebox.showerror("Error",item)
      return
   searchL12["text"] = str(item[0])#insert name
   searchL13["text"] = str(item[1])#insert description
   searchL14["text"] = str(item[4][0])#insert storage name
   searchL15["text"] = str(item[4][1])# insert shelve number
   searchL16["text"] = str(item[4][2])# insert partition number
   searchL17["text"] = str(item[2])#insert amount

   #---Convert 0/1 to "yes"/"no"--
   if item[3] == 0:
      autoOrder = "Nein"
   else:
      autoOrder = "Ja"
   #------------------------------

   searchL18["text"] = autoOrder#insert auto Order

#---------------------------------------------------------------------------------------------------------

#--------------------get storage entrys----------------------------------------------------------------

def readStorage(layer,department = ""):
   #-Setup-------
   storages = []
   #-------------
   storageRead =selectAllStorage()#read storage

   #-->extract storages-----------------------------------------------------
   if layer == "storages":
      for storage in storageRead:#for every Storage...
         storages.append(storage[0])#...put the name in the array
   #------------------------------------------------------------------------

   #-->extract shelves------------------------------------------------------
   elif layer == "shelves":
      for storage in storageRead:#extract storage

         if department == "":#if return all shelves ...
            for shelve in storage[1]:#...for every shelve in storage...
               storages.append(shelve[0])#...get the name in an array

         else:#if return a specific shelve
            if str(storage[0]) == department:# when the storage is found...
               for shelve in storage[1]:#...for every shelve in storage...
                  storages.append(shelve[0])#...get the name in an array
   #-------------------------------------------------------------------------

   #-->extract partitions---------------------------------------------------------------------------------------------
   elif layer == "partitions":

      for storage in storageRead:#extract storage
         for shelve in storage[1]:#extract shelves

            if department == "":#if return all partitions
               for partition in shelve[1]:# for every shelve in storage...
                  storages.append(partition)#...get all the partitions and put them in the array


            else:#if return a specific partition
               if str(shelve[0]) == department:#if the shelve given is found...
                  for partition in shelve[1]:# for the shelve in storage that matches the shelve given as parameter...
                     storages.append(partition)#...get all the partitions and put them in the array
   #--------------------------------------------------------------------------------------------------------------------

   return storages #return

def getValidShelves(shelveEntry,storageEntry,partitionEntry):
   shelveEntry['values'] = readStorage("shelves",str(storageEntry.get()))#get shelves,assign values
   clearComboboxEntrys(partitionEntry)# clear entry of partition combobox, it could be invalid now



def getValidPartitions(partitionEntry,shelveEntry):
   partitionEntry['values'] = readStorage("partitions",str(shelveEntry.get()))#get partitons,assign values

#-------------------------------------------------------------------------------------------------------

#-------------edit functions-----------------------------------------------------------------------------
def edit():
   if searchL12["text"] == "":# if search() wasn't called beforhand
      messagebox.showerror("Fehler", "Es wurde kein Gegenstand zum Bearbeiten ausgewählt" )# own error report
      return# cancel

   searchB2.place_forget()
   searchE2.config(state = "disabled")# the name in this entry is later used to call other functions, if changed by user it will not work, disabeling this entry prevents the interference of the user

   searchE4.config(state = "normal")
   searchE4.place(x = 165, y = 20)#place the entry
   searchE4.delete(0,END)#pushing edit multiple tims would result in the entry getting filled over in over again with information, it needs to be cleared
   searchE4.insert(0,searchL12["text"])#insert name from lable
   searchE4.config(state = "disabled")# user isnt allowed to change the name

   searchE5.place(x = 165, y = 50)#place the entry
   searchE5.delete(0,END)#pushing edit multiple tims would result in the entry getting filled over in over again with information, it needs to be cleared
   searchE5.insert(0,searchL13["text"])#insert description from lable

   #Comboboxes can't have multiple informations inserted so they don't need clearing:
   storageOptionsComboboxEditItem.place(x = 165, y = 140)#place the combobox
   storageOptionsComboboxEditItem.set(searchL14["text"])#insert storageName from lable

   shelveOptionsComboboxEditItem.place(x = 165, y = 170)#place the combobox
   shelveOptionsComboboxEditItem.set(searchL15["text"])#insert shelveNumber from lable

   partitionOptionsComboboxEditItem.place(x = 165, y = 200)#place the combobox
   partitionOptionsComboboxEditItem.set(searchL16["text"])#insert partiotionNumber from lable

   searchSB1.place(x = 165, y = 230)#place the scrollbox
   searchSB1.delete(0,END)#pushing edit multiple times would result in the entry getting filled over in over again with information, it needs to be cleared
   searchSB1.insert(0,searchL17["text"])#insert amount

   searchCB1.place(x = 160, y = 260)#place checkbox for auto order
   if searchL18["text"] == "Ja":#if autoOrder is 1
      searchCB1.select()#select checkbox
   else:#else deselct it.
      searchCB1.deselect()

   buttonDeleteSearchItemEdit.place(x = 500, y = 402)#place new button "delete item"
   searchB3.place(x = 660, y = 402)#place new button "cancel"
   searchB4.place(x = 580, y = 402)#place new button "save edit"

def cancel():#self explaning
   searchE2.config(state = "active")
   searchE4.place_forget()
   searchE5.place_forget()
   storageOptionsComboboxEditItem.place_forget()
   shelveOptionsComboboxEditItem.place_forget()
   partitionOptionsComboboxEditItem.place_forget()
   searchSB1.place_forget()
   searchCB1.place_forget()
   searchB3.place_forget()
   searchB4.place_forget()
   buttonDeleteSearchItemEdit.place_forget()
   searchB2.place(x = 660, y = 402)

def GUIcreateStorage():
   createStorageNameEntry.place(x=165,y=20)
   createStorageNameEntry.delete(0,END)
   createStorageDescriptionEntry.place(x=165,y=50)
   createStorageDescriptionEntry.delete(0,END)
   createStorageConfirm.place(x =550, y = 25)

def editStorage():
   storageEditEntryName.place(x=165,y=20)
   storageEditEntryName.config(state = "normal")
   storageEditEntryName.delete(0,END)
   storageEditEntryName.insert(0,storageNameEntryLabel["text"])
   storageEditEntryName.config(state = "disabled")

   storageEditEntryDescription.place(x=165,y=50)
   storageEditEntryDescription.delete(0,END)
   storageEditEntryDescription.insert(0,storageDescriptionEntryLabel["text"])

   editStorageCancel.place(x =550, y = 25)

   editStorageSave.place(x =650, y = 25)

def cancelStorageEdit():
   storageEditEntryName.place_forget()
   storageEditEntryDescription.place_forget()
   editStorageCancel.place_forget()
   editStorageSave.place_forget()

def GUIcreateShelve():
   pass

def editShelve():
   storageOptionsComboboxEditShelve.place(x = 165, y = 50)
   editShelvesCancel.place(x =550, y = 25)
   editShelvesSave.place(x =650, y = 25)
   shelvesEditEntryName.place(x=165,y=20)
   shelvesEditEntryName.config(state = "normal")
   shelvesEditEntryName.delete(0,END)
   shelvesEditEntryName.insert(0,shelvesNameEntryLabel["text"])
   shelvesEditEntryName.config(state = "disabled")

def cancelShelveEdit():
   storageOptionsComboboxEditShelve.place_forget()
   editShelvesCancel.place_forget()
   editShelvesSave.place_forget()
   shelvesEditEntryName.place_forget()

def GUIcreatePartition():
   pass

def editPartition():
   storageOptionsComboboxEditPartition.place(x = 165, y = 50)

   editPartitionsCancel.place(x =550, y = 25)
   editPartitionsSave.place(x =650, y = 25)

   partitionsEditEntryName.place(x=165,y=20)
   partitionsEditEntryName.config(state = "normal")
   partitionsEditEntryName.delete(0,END)
   partitionsEditEntryName.insert(0,partitionsNameEntryLabel["text"])
   partitionsEditEntryName.config(state = "disabled")

def cancelPartitionEdit():
   storageOptionsComboboxEditPartition.place_forget()
   editPartitionsCancel.place_forget()
   editPartitionsSave.place_forget()
   partitionsEditEntryName.place_forget()
#------------------------------------------------------------------------------------------------------------------------------

# --- Fenster -----------------------------------------------------------------------
root = Tk()
root.configure(height=460,width=800)
root.title('ProStorage System')
root.resizable(width=NO, height=NO)
#img = PhotoImage(file='Noppa2.gif')
#root.tk.call('wm', 'iconphoto', root._w, img)
# -----------------------------------------------------------------------------------

# ------ Dropdownmenu ---------------------------------------------------------------
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import")
filemenu.add_command(label="Export")

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="Lagersystem", menu=filemenu)

root.config(menu=menubar)
# -----------------------------------------------------------------------------------

# --- Tabs --------------------------------------------------------------------------
tabs = ttk.Notebook(root)
tabs.place(x = 0, y = 0)

allF = ttk.Frame(height=460,width=800)
searchF = ttk.Frame(height=460,width=800)
createF = ttk.Frame(height=460,width=800)
storageF = ttk.Frame(height=460,width=800)
manageStorage = ttk.Frame(height=460,width=800)

tabs.add(allF, text='     Alle Teile     ')
tabs.add(searchF, text='     Teil suchen     ')
tabs.add(createF, text='     Teil erstellen     ')
tabs.add(storageF, text='        Lager        ')
tabs.add(manageStorage, text='       Lager verwalten       ')
# -----------------------------------------------------------------------------------

# --- Alle Teile --------------------------------------------------------------------
itemListTreeview = ttk.Treeview(allF)
itemListTreeview['columns'] = ( 'Lagerplatz','Anzahl',"Auto-Bestellen",)

itemListTreeview.column('Lagerplatz', anchor='w')
itemListTreeview.heading('Lagerplatz', text='Lagerplatz')

itemListTreeview.column('Anzahl', anchor='w')
itemListTreeview.heading('Anzahl', text='Anzahl')

itemListTreeview.column('Auto-Bestellen', anchor='w')
itemListTreeview.heading('Auto-Bestellen', text='Auto-Bestellen')

scrollbarTreeviewY = ttk.Scrollbar(allF, orient='vertical', command=itemListTreeview.yview)
itemListTreeview.configure(yscroll=scrollbarTreeviewY.set)
itemListTreeview.bind("<Double-1>", itemListTreeviewOnDoubleClick)
scrollbarTreeviewY.pack(side = RIGHT, fill = Y)

itemListTreeview.place(x=0, y=0,height = 445, width = 785)

populateItemTreeview()

# ---------------------------------------------------------------------------------

# --- Teil suchen -----------------------------------------------------------------
searchLabelframeSearchResults = ttk.Labelframe(searchF, text="Suchergebnisse", height=80, width=375)
searchLabelframeSearchResults.place(x=400,y= 5)

searchResultsTreeview = ttk.Treeview(searchLabelframeSearchResults)
searchResultsTreeview['columns'] = ( 'Beschreibung')

searchResultsTreeview.column('Beschreibung', anchor='w')
searchResultsTreeview.heading('Beschreibung', text='Beschreibung')

scrollbarTreeviewYSearchResults = ttk.Scrollbar(searchLabelframeSearchResults, orient='vertical', command=searchResultsTreeview.yview)
searchResultsTreeview.configure(yscroll=scrollbarTreeviewYSearchResults.set)
searchResultsTreeview.bind("<Double-1>", searchResultTreeviewOnDoubleClick)

scrollbarTreeviewYSearchResults.place(x=355,y=4)

searchResultsTreeview.place(x=0, y=0,height = 57,width=365)

searchSF = ttk.Labelframe(searchF, text='Item-Parameter',height=315, width=750)
searchSF.place(x = 25, y = 80)


searchL2 = Label(searchF, font=(18), text='Teile-Name :')
searchL2.place(x = 10, y = 25)

searchE2 = ttk.Entry(searchF, font=(18))
searchE2.place(x = 125, y = 25)

searchB1 = ttk.Button(searchF, text='Suchen', command = lambda: search(searchE2))
searchB1.place(x = 320, y = 25)
searchB2 = ttk.Button(searchF, text='Bearbeiten', command = lambda: edit())
searchB2.place(x = 660, y = 402)


searchL4 = Label(searchSF, font=(18), text='Teile-Name :')
searchL4.place(x = 10, y = 20)
searchL5 = Label(searchSF, font=(18), text='Beschreibung :')
searchL5.place(x = 10, y = 50)
searchL6 = Label(searchSF, font=(18), text='Lager :')
searchL6.place(x = 10, y = 140)
searchL7 = Label(searchSF, font=(18), text='Regal-Nummer :')
searchL7.place(x = 10, y = 170)
searchL8 = Label(searchSF, font=(18), text='Abteilungs-Nummer :')
searchL8.place(x = 10, y = 200)
searchL9 = Label(searchSF, font=(18), text='Anzahl :')
searchL9.place(x = 10, y = 230)
searchL10 = Label(searchSF, font=(18), text='Auto. Bestellung :')
searchL10.place(x = 10, y = 260)



searchL12 = Label(searchSF, font=(18), text='')
searchL12.place(x = 165, y = 20)
searchL13 = Label(searchSF, font=(18), text='')
searchL13.place(x = 165, y = 50)
searchL14 = Label(searchSF, font=(18), text='')
searchL14.place(x = 165, y = 140)
searchL15 = Label(searchSF, font=(18), text='')
searchL15.place(x = 165, y = 170)
searchL16 = Label(searchSF, font=(18), text='')
searchL16.place(x = 165, y = 200)
searchL17 = Label(searchSF, font=(18), text='')
searchL17.place(x = 165, y = 230)
searchL18 = Label(searchSF, font=(18), text='')
searchL18.place(x = 165, y = 260)



searchE4 = Entry(searchSF, font=(18))#name
searchE4.place()
searchE5 = Entry(searchSF, font=(18),width=50)#description
searchE5.place()


storageEditItem = StringVar()#storage var
storageOptionsComboboxEditItem = ttk.Combobox(searchSF, textvariable = storageEditItem,postcommand=lambda:clearComboboxEntrys(shelveOptionsComboboxEditItem,partitionOptionsComboboxEditItem))#storage entry
storageOptionsComboboxEditItem['values'] = readStorage("storages")#get storages, assign values
storageOptionsComboboxEditItem.place()#place

shelveEditItem = StringVar()#shelve var
shelveOptionsComboboxEditItem = ttk.Combobox(searchSF, textvariable = shelveEditItem, postcommand = lambda:getValidShelves(shelveOptionsComboboxEditItem,storageOptionsComboboxEditItem,partitionOptionsComboboxEditItem))#shelve entry
#values get assigned in postcommand
shelveOptionsComboboxEditItem.place()#place

partitionEditItem = StringVar()#partition  var
partitionOptionsComboboxEditItem = ttk.Combobox(searchSF, textvariable = partitionEditItem, postcommand = lambda:getValidPartitions(partitionOptionsComboboxEditItem,shelveOptionsComboboxEditItem))#partition entry
#values get assigned in postcommand
partitionOptionsComboboxEditItem.place()#place


searchSB1 = Spinbox(searchSF, font=(18), from_=0, to=13000000000000000001337)
searchSB1.place()

sCB1 = IntVar()
searchCB1 = Checkbutton(searchSF, variable = sCB1, onvalue = 1, offvalue = 0)
searchCB1.place()

buttonDeleteSearchItemEdit = ttk.Button(searchF, text= "Löschen",command = lambda: GUIdeleteItem(searchL12))
buttonDeleteSearchItemEdit.place()

searchB3 = ttk.Button(searchF, text='Abbrechen', command = lambda: cancel())
searchB3.place()
searchB4 = ttk.Button(searchF, text='Speichern', command = lambda: saveEdit(searchL12,searchE5,storageOptionsComboboxEditItem,shelveOptionsComboboxEditItem,partitionOptionsComboboxEditItem,searchSB1,sCB1))
searchB4.place()

# -----------------------------------------------------------------------------------

# --- Teil erstellen ----------------------------------------------------------------

createSF = ttk.Labelframe(createF, text='Gegenstand-Eigenschaften',height=315, width=750)
createSF.place(x = 25, y = 80)


createL2 = Label(createSF, font=(18), text='Teile-Name :')
createL2.place(x = 10, y = 20)
createL3 = Label(createSF, font=(18), text='Beschreibung :')
createL3.place(x = 10, y = 50)
createL4 = Label(createSF, font=(18), text='Lager :')
createL4.place(x = 10, y = 140)
createL5 = Label(createSF, font=(18), text='Regal-Nummer :')
createL5.place(x = 10, y = 170)
createL6 = Label(createSF, font=(18), text='Abteilungs-Nummer :')
createL6.place(x = 10, y = 200)
createL7 = Label(createSF, font=(18), text='Anzahl :')
createL7.place(x = 10, y = 230)
createL8 = Label(createSF, font=(18), text='Auto. Bestellung :')
createL8.place(x = 10, y = 260)


createE2 = ttk.Entry(createSF, font=(18))#Name
createE2.place(x = 165, y = 20)
createE3 = ttk.Entry(createSF, font=(18), width=50)#Beschreibung
createE3.place(x = 165, y = 50)


storageCreateItem = StringVar()#storage var
storageOptionsComboboxCreateItem = ttk.Combobox(createSF, textvariable = storageCreateItem, postcommand = lambda:clearComboboxEntrys(partitionOptionsComboboxCreateItem,shelveOptionsComboboxCreateItem))#storage entry
storageOptionsComboboxCreateItem['values'] = readStorage("storages")#get storages, assign values
storageOptionsComboboxCreateItem.place(x = 165, y = 140)#place

shelveCreateItem = StringVar()#shelve var
shelveOptionsComboboxCreateItem = ttk.Combobox(createSF, textvariable = shelveCreateItem, postcommand = lambda:getValidShelves(shelveOptionsComboboxCreateItem,storageOptionsComboboxCreateItem,partitionOptionsComboboxCreateItem))#shelve entry
#values get assigned in postcommand
shelveOptionsComboboxCreateItem.place(x = 165, y = 170)#place

partitionCreateItem = StringVar()#partition  var
partitionOptionsComboboxCreateItem = ttk.Combobox(createSF, textvariable = partitionCreateItem, postcommand = lambda:getValidPartitions(partitionOptionsComboboxCreateItem,shelveOptionsComboboxCreateItem))#partition entry
#values get assigned in postcommand
partitionOptionsComboboxCreateItem.place(x = 165, y = 200)#place

createSB1 = Spinbox(createSF, font=(18), from_=0, to=13000000000000000001337)
createSB1.place(x = 165, y = 230)

cCB1 = IntVar()
createCB1 = Checkbutton(createSF, variable = cCB1, onvalue = 1, offvalue = 0)
createCB1.place(x = 160, y = 260)

createB2 = ttk.Button(createF, text='Erstellen', command = lambda: insertItem(createE2, createE3, storageOptionsComboboxCreateItem,shelveOptionsComboboxCreateItem, partitionOptionsComboboxCreateItem, cCB1, createSB1))
createB2.place(x = 660, y = 402)

# -----------------------------------------------------------------------------------

# --- Lager -------------------------------------------------------------------------

storageListTreeview = ttk.Treeview(storageF)
storageListTreeview['columns'] = ( 'Beschreibung')

storageListTreeview.column('Beschreibung', anchor='w')
storageListTreeview.heading('Beschreibung', text='Beschreibung')

scrollbarTreeviewY = ttk.Scrollbar(storageF, orient='vertical', command=storageListTreeview.yview)
storageListTreeview.configure(yscroll=scrollbarTreeviewY.set)
storageListTreeview.bind("<Double-1>", storageListTreeviewOnDoubleClick)
scrollbarTreeviewY.pack(side = RIGHT, fill = Y)

storageListTreeview.place(x=0, y=0,height = 445, width = 785)

populateStorageTreeview()

# ------------------------------------------------------------------------------------

# --- LAger verwalten ----------------------------------------------------------------------

storageTabs = ttk.Notebook(manageStorage)
storageTabs.place(x = 0, y = 0)

manageStorageStorages = ttk.Frame(height=460,width=800)
manageShelves = ttk.Frame(height=460,width=800)
managePartitions = ttk.Frame(height=460,width=800)

storageTabs.add(manageStorageStorages, text='     Lager verwalten     ')
storageTabs.add(manageShelves, text='     Regale verwalten     ')
storageTabs.add(managePartitions, text='     Abteile verwalten     ')

###---Lager verwalten------------------------------------------------------------------------
manageStorageStoragesFrame = ttk.Labelframe(manageStorageStorages, text='Lager-Parameter',height=315, width=750)
manageStorageStoragesFrame.place(x = 25, y = 80)

searchStorage = Label(manageStorageStorages, font=(18), text='Lager-Name :')
searchStorage.place(x = 10, y = 25)

searchStorageEntry = ttk.Entry(manageStorageStorages, font=(18))
searchStorageEntry.place(x = 125, y = 25)

searchB1 = ttk.Button(manageStorageStorages, text='Suchen', command = lambda: GUIselectStorage(searchStorageEntry))
searchB1.place(x = 320, y = 25)

createStorageButton = ttk.Button(manageStorageStorages, text='Erstellen', command = GUIcreateStorage)
createStorageButton.place(x =550, y = 25)

createStorageConfirm = ttk.Button(manageStorageStorages, text='Bestätigen', command = lambda:createStorage(createStorageNameEntry,createStorageDescriptionEntry))


createStorageNameEntry = ttk.Entry(manageStorageStoragesFrame, font=(18))
createStorageDescriptionEntry = ttk.Entry(manageStorageStoragesFrame, font=(18))

editStorage = ttk.Button(manageStorageStorages, text='Bearbeiten', command = editStorage)
editStorage.place(x =650, y = 25)

storageName = Label(manageStorageStoragesFrame, font=(18), text='Name :')
storageName.place(x = 10, y = 20)
storageDescription = Label(manageStorageStoragesFrame, font=(18), text='Beschreibung :')
storageDescription.place(x = 10, y = 50)

storageNameEntryLabel = Label(manageStorageStoragesFrame, font=(18), text='')
storageNameEntryLabel.place(x = 165, y = 20)
storageDescriptionEntryLabel = Label(manageStorageStoragesFrame, font=(18), text='')
storageDescriptionEntryLabel.place(x = 165, y = 50)

storageEditEntryName = ttk.Entry(manageStorageStoragesFrame,font=(18))
storageEditEntryDescription = ttk.Entry(manageStorageStoragesFrame,font=(18))
editStorageCancel = ttk.Button(manageStorageStorages, text='Abbrechen', command = cancelStorageEdit)
editStorageSave = ttk.Button(manageStorageStorages, text='Speichern', command = lambda:saveStorageEdit(storageEditEntryName,storageEditEntryDescription))
###------------------------------------------------------------------------------------------

###---Regale verwalten------------------------------------------------------------------------
manageShelvesFrame = ttk.Labelframe(manageShelves, text='Regal-Parameter',height=315, width=750)
manageShelvesFrame.place(x = 25, y = 80)

searchShelves = Label(manageShelves, font=(18), text='Regal-Nummer :')
searchShelves.place(x = 10, y = 25)

searchShelvesEntry = ttk.Entry(manageShelves, font=(18))
searchShelvesEntry.place(x = 125, y = 25)

searchB1 = ttk.Button(manageShelves, text='Suchen', command = lambda: GUIselectShelve(searchShelvesEntry))
searchB1.place(x = 320, y = 25)

createShelves = ttk.Button(manageShelves, text='Erstellen')
createShelves.place(x =550, y = 25)

editShelve = ttk.Button(manageShelves, text='Bearbeiten', command = editShelve)
editShelve.place(x =650, y = 25)

shelvesName = Label(manageShelvesFrame, font=(18), text='Nummer :')
shelvesName.place(x = 10, y = 20)
shelvesDescription = Label(manageShelvesFrame, font=(18), text='Lager :')
shelvesDescription.place(x = 10, y = 50)

shelvesNameEntryLabel = Label(manageShelvesFrame, font=(18), text='')
shelvesNameEntryLabel.place(x = 165, y = 20)
shelvesDescriptionEntryLabel = Label(manageShelvesFrame, font=(18), text='')
shelvesDescriptionEntryLabel.place(x = 165, y = 50)

shelvesEditEntryName = ttk.Entry(manageShelvesFrame,font=(18))

storageEditShelve = StringVar()#storage var
storageOptionsComboboxEditShelve = ttk.Combobox(manageShelvesFrame, textvariable = storageEditShelve)#storage entry
storageOptionsComboboxEditShelve['values'] = readStorage("storages")#get storages, assign values

editShelvesCancel = ttk.Button(manageShelves, text='Abbrechen', command = cancelShelveEdit)
editShelvesSave = ttk.Button(manageShelves, text='Speichern', command = lambda:saveShelveEdit(shelvesEditEntryName,storageEditShelve))
###------------------------------------------------------------------------------------------

###---Partitionen verwalten------------------------------------------------------------------------
managePartitionsFrame = ttk.Labelframe(managePartitions, text='Abteil-Parameter',height=315, width=750)
managePartitionsFrame.place(x = 25, y = 80)

searchPartitions = Label(managePartitions, font=(18), text='Abteil-Nummer :')
searchPartitions.place(x = 10, y = 25)

searchPartitionsEntry = ttk.Entry(managePartitions, font=(18))
searchPartitionsEntry.place(x = 125, y = 25)

searchB1 = ttk.Button(managePartitions, text='Suchen', command = lambda: GUIselectPartition(searchPartitionsEntry))
searchB1.place(x = 320, y = 25)

createPartitions = ttk.Button(managePartitions, text='Erstellen')
createPartitions.place(x =550, y = 25)

editPartition = ttk.Button(managePartitions, text='Bearbeiten', command = editPartition)
editPartition.place(x =650, y = 25)

partitionsName = Label(managePartitionsFrame, font=(18), text='Nummer :')
partitionsName.place(x = 10, y = 20)
partitionsDescription = Label(managePartitionsFrame, font=(18), text='Regal :')
partitionsDescription.place(x = 10, y = 50)

partitionsNameEntryLabel = Label(managePartitionsFrame, font=(18), text='')
partitionsNameEntryLabel.place(x = 165, y = 20)
partitionsDescriptionEntryLabel = Label(managePartitionsFrame, font=(18), text='')
partitionsDescriptionEntryLabel.place(x = 165, y = 50)

storageEditPartition = StringVar()#storage var
storageOptionsComboboxEditPartition = ttk.Combobox(managePartitionsFrame, textvariable = storageEditPartition)#storage entry
storageOptionsComboboxEditPartition['values'] = readStorage("shelves")#get storages, assign values

partitionsEditEntryName = ttk.Entry(managePartitionsFrame,font=(18))
partitionsEditEntryDescription = ttk.Entry(managePartitionsFrame,font=(18))
editPartitionsCancel = ttk.Button(managePartitions, text='Abbrechen', command = cancelPartitionEdit)
editPartitionsSave = ttk.Button(managePartitions, text='Speichern', command = lambda:savePartitionEdit(partitionsEditEntryName,storageEditPartition))
###------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------
#root.mainloop()


