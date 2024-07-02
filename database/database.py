#TODO : change value



import json

DB = "database.json" #path to database




def readPlaces():
    with open(DB, 'r') as db:
        data = json.load(db)
        for i in data:
            print(i)

def addPlace( MAC:str, Connected:bool, name:str="Noname", LastIP:str=None, CurrentIP=None):
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
            data = removeEntries(data, "MAC", MAC)

        data.append({"name" : name, "Connected":Connected, "MAC":MAC, "IP": CurrentIP, "LastIP":LastIP})
        print(data,"\n")
        db.seek(0)
        json.dump(data, db, indent=4)
        db.truncate()

def removePlace(name):
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

def delete_data():    # Deletes an element from the array
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
def removeEntries(data, key, value):
    return [entry for entry in data if entry.get(key) != value]




#removePlace('test')

