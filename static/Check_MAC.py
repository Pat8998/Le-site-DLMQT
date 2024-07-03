from flask import Flask, request
import threading
from scapy.all import ARP, Ether, srp, sniff

Whitelist = ["f4:09:d8:64:b0:8e", "6c:62:6d:97:15:b4"]






mac_addresses = {}

def get_mac(ip_address):
    """
    Actively request the MAC address of the specified IP address using ARP.
    """
    if ip_address in mac_addresses:
        return mac_addresses[ip_address]

    # Create an ARP request packet
    arp_request = ARP(pdst=ip_address)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Send the ARP request and wait for a response
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    for sent, received in answered_list:
        mac_addresses[ip_address] = received.hwsrc
        return received.hwsrc

    return None

def arp_display(pkt):
    """
    Callback function to process sniffed packets.
    """
    if pkt[ARP].op == 1:  # who-has (request)
        return
    if pkt[ARP].op == 2:  # is-at (response)
        mac_addresses[pkt[ARP].psrc] = pkt[ARP].hwsrc

def start_sniffing():
    """
    Start sniffing ARP packets in a separate thread.
    """
    sniff(filter="arp", prn=arp_display, store=0)

def Check_MAC(ip):
    mac = get_mac(ip)
    return True if mac in Whitelist else False