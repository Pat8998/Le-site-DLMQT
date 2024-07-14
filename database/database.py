import os
import json

DB = "database.json" #path to database
DB = os.path.dirname(os.path.abspath(__file__))+'\\'+DB



def ReadPlaces():
    with open(DB, 'r') as db:
        data = json.load(db)
        for i in data:
            print(i)

def AddEntry( MAC:str, Connected:bool, name:str="Noname", LastIP:str=None, CurrentIP=None, Blacklist:bool=False, VIP:bool=False):
    with open(DB, 'r+') as db:
        data = json.load(db)
        if data != []:
            for entry in data:
                if entry['MAC']==MAC:        #Refresh if MAC already exists
                    if LastIP==None :      #check to keep the data if no fresh one Has been detected
                          LastIP=entry[LastIP]
                    if CurrentIP==None :      #check to keep the data if no fresh one Has been detected
                          CurrentIP=entry[IP]
                    if name=="Noname" :      #check to keep the data if no fresh one Has been detected
                          name=entry[name]
            data = RemoveEntries(data, "MAC", MAC)

        data.append({"name" : name, "Connected":Connected, "MAC":MAC, "IP": CurrentIP, "LastIP":LastIP, "Blacklisted": Blacklist, "VIP":VIP})
        print(data,"\n")
        db.seek(0)
        json.dump(data, db, indent=4)
        db.truncate()
        
def ChangeValue(MAC: str, Connected: bool = None, name: str = None, LastIP: str = None, CurrentIP: str = None, Blacklist: bool = None, VIP: bool = None):
    #print(f"ChangeValue called with MAC: {MAC}, Connected: {Connected}, name: {name}, LastIP: {LastIP}, CurrentIP: {CurrentIP}, Blacklist: {Blacklist}, VIP: {VIP}")
    with open(DB, 'r+') as db:
        data = json.load(db)
        if data:
            for entry in data:
                if entry['MAC'] == MAC:  # Refresh if MAC already exists
                    if LastIP is None:
                        LastIP = entry['LastIP']
                    if CurrentIP is None:
                        CurrentIP = entry['IP']
                    if name is None:
                        name = entry['name']
                    if Connected is None:
                        Connected = entry['Connected']
                    if Blacklist is None:
                        Blacklist = entry['Blacklisted']
                    if VIP is None:
                        VIP = entry['VIP']

                    # Update the entry
                    entry.update({
                        "name": name,
                        "Connected": Connected,
                        "MAC": MAC,
                        "IP": CurrentIP,
                        "LastIP": LastIP,
                        "Blacklisted": Blacklist,
                        "VIP": VIP
                    })
                    #print(f"Updated entry: {entry}")

                    # Write the updated data back to the JSON file
                    db.seek(0)
                    json.dump(data, db, indent=4)
                    db.truncate()
                    return
            print("ERROR: Can't change data if it doesn't exist yet")
        else:
            print("ERROR: No data found in the database")


def RemoveEntry(name):
    new_data = []
    with open(DB, 'r+') as db:
        data = json.load(db)
        i=0
        for dict in data:
                if dict['MAC']!=name and dict['name']!=name: #added MAC deletion
                        print('keeping', data[i])
                        new_data.append(dict)
                i+=1
        db.seek(0)
        print(new_data)
        with open(DB, "w") as db:
            json.dump(new_data, db, indent=4)

def DeleteData():    # Deletes an element from the array
    new_data = []
    with open(DB, "r") as f:
        data = json.load(f)
        data_length = len(data) - 1
    print("Which index number would you like to delete?")
    delete_option = input(f"Select a number 0-{data_length}: ")
    i = 0
    for entry in data:
        print(entry)
        if i == int(delete_option):
            i += 1
        else:
            new_data.append(entry)
            i +=  1
    print(new_data)
    with open(DB, "w") as f:
        json.dump(new_data, f, indent=4)

# Function to remove entries based on a condition
def RemoveEntries(data, key, value):
    return [entry for entry in data if entry.get(key) != value]





