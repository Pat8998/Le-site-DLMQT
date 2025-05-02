import json
import os
import subprocess
from time import sleep
from threading import Event
from queue import Queue

stop_thread = False
ignore_event = Event()
communication_queue = Queue()
db_path = os.path.join(os.path.dirname(__file__), '..','database', 'database.json')

# Load devices from database/database.json
def load_devices():
    try:
        #ignore_event.set()
        communication_queue.put(True)
        #print("loading : database")
        with open(db_path, 'r') as file:
            devices = json.load(file)
    except FileNotFoundError:
        devices = []
    ignore_event.clear()
    #sleep(0.2)
    #communication_queue.put(None)
    return devices

# Save devices to database/database.json
def save_devices(devices):
    print("updating database")
    with open(db_path, 'w') as file:
        json.dump(devices, file, indent=4)

# Find a device in the database by its MAC address
def find_device_by_mac(devices, mac):
    for device in devices:
        if device['MAC'] == mac:
            return device
    return None

# Add or update a device in the database
def add_or_update_device(devices, mac, ip=None, name=None, connected=True):
    device = find_device_by_mac(devices, mac)
    if device:
        # Update existing device
        device['LastIP'] = device['IP']
        device['IP'] = ip
        device['Connected'] = connected
    else:
        # Add new device
        new_device = {
            "name": name,
            "Connected": connected,
            "MAC": mac,
            "IP": ip,
            "LastIP": "",
            "Blacklisted": False,  # Default value for new devices
            "VIP": False           # Default value for new devices
        }
        devices.append(new_device)

# Disconnect a blacklisted device using aireplay-ng
def disconnect_blacklisted_device(mac, interface):
    command = f"aireplay-ng --deauth 5 -c {mac} {interface}"
    os.system(command)
    print(f"Disconnected blacklisted device with MAC: {mac}")

# Check for blacklisted devices and disconnect them
def check_blacklisted_devices(devices, interface):
    for device in devices:
        if device['Connected'] and device['Blacklisted']:
            disconnect_blacklisted_device(device['MAC'], interface)
            device['Connected'] = False

# Get hostname of a device using nmap
def get_device_name(ip):
    try:
        # Use nmap to find the hostname
        result = subprocess.run(['nmap', '-sn', ip], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'Nmap scan report for' in line:
                return line.split('for ')[-1]  # Extract hostname
    except Exception as e:
        print(f"Error in nmap: {e}")
    
    return f"Unknown_{ip}"  # Default if no name is found

# Monitor real-time connected devices via 'iw dev <interface> station dump'
def monitor_connections(interface):
    command = f"iw dev {interface} station dump"
    result = subprocess.run(command.split(), capture_output=True, text=True)
    
    connected_devices = []
    
    # Parse the output to extract MAC addresses
    current_mac = None
    for line in result.stdout.splitlines():
        if "Station" in line:
            current_mac = line.split()[1]  # Extract MAC address
            ip = f"192.168.1.{len(connected_devices) + 2}"  # Assign IPs in sequence
            connected_devices.append({"mac": current_mac, "ip": ip})
    
    return connected_devices

# Main function to update the database and manage connections
def manage_network(interface):
    old_devices = load_devices()
    devices = load_devices()
    # Monitor connections and update the database
    connected_devices = monitor_connections(interface)
    for device_info in devices:
        add_or_update_device(devices, device_info['MAC'], connected=False)
    
    for device_info in connected_devices:
        mac = device_info["mac"]
        ip = device_info["ip"]
        
        # Get the name of the device (hostname)
        name = get_device_name(ip)
        
        # Add or update device information
        add_or_update_device(devices, mac, ip, name, connected=True)
    
    # Check for any blacklisted devices and disconnect them
    check_blacklisted_devices(devices, interface)


    #print("old devices :", old_devices)

    #print("devices :", devices)


    # Save the updated devices list
    if devices != old_devices :
        print("old devices :", old_devices)

        print("devices :", devices)

        save_devices(devices)
    

def network_manage():
    # Replace with your Wi-Fi interface in monitor mode
    wifi_interface = "phy0-ap0"
    print("starting manager..")
    global stop_thread    
    # Continuously monitor and manage network connections
    while not stop_thread :
        manage_network(wifi_interface)
        sleep(0.5)

if __name__ == "__main__":
	network_manage()
