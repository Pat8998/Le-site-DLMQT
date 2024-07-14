# from LefichierdeMatyu import *
from database.database import *

def Disconnect(device):
    #Matyu puts his funcion right her
    ChangeValue(device, Connected=False) #just a place holder

def server_change_priority(device, priority_type, previous_value:bool):
    # Convert JavaScript boolean strings to Python boolean values
    if previous_value.lower() == 'true':
        previous_value = True
    elif previous_value.lower() == 'false':
        previous_value = False
    else:
        raise ValueError("Invalid value for previous_value: must be 'true' or 'false'")
    if priority_type == 'blacklist':
        print ("Changing blacklist of " + device +' into ' + str(not previous_value))
        ChangeValue(device, Blacklist= not previous_value)
    else : #elif priority_type == 'VIP':
        print ("Changing VIP of " + device +' into ' + str(not previous_value))
        ChangeValue(device, VIP= not previous_value)