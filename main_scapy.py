import importlib
import os
import pathlib
import re

from scapy.all import *

from ankama.DofusPacket import DofusPacket

############################################
### UNIQUE UID WINDOWS ETH
############################################
ethernetNicUUID = '\\Device\\NPF_{AC96C4C9-D4B2-4ABD-A5FC-8F5BC32BF1F0}'

############################################
### CREATE CORRESPONDENCE IF NOT EXIST
############################################
if not os.path.isfile("correspondance.txt"):
    with open("utils/findIds.py") as file:
        exec(file.read())

if os.stat("correspondance.txt").st_size == 0:
    with open("utils/findIds.py") as file:
        exec(file.read())

############################################
### LOAD ALL CLASS OF CUSTOM MESSAGES
############################################
messageClasses = {}
current_path = pathlib.Path().resolve()
print("STARTING ALL MESSAGE CLASS IMPORT")
for root, dirs, files in os.walk("ankama/messages"):
    for file in files:
        if file != "__init__.py":
            newRoot = root.removeprefix(str(current_path)).replace('\\', '/').replace('/', '.')
            if not re.match(r".*pycache.*", newRoot):
                print(f"\timporting: {file[:-3]} from {newRoot}")
                messageClasses[file[:-3]] = importlib.import_module(f".{file[:-3]}", newRoot)
print("\n")

print("STARTING SNIFFING")


def newCallback(raw_packet):
    if "TCP" in raw_packet:
        direction = None
        if raw_packet["TCP"].sport == 5555:
            direction = "to_client"
        if raw_packet["TCP"].dport == 5555:
            direction = "from_client"
        if direction is not None:
            # payload = getattr(raw_packet.tcp, 'payload', None)
            # payload = getattr(raw_packet.tcp, 'data', None)
            payload = None
            try:
                payload = bytes(raw_packet["TCP"].payload)
            except:
                print("no data")
            if payload:
                first_two_bytes = payload[:2]
                hiheader = int.from_bytes(first_two_bytes, byteorder='big', signed=False)
                packetId = hiheader >> 2
                lengthType = hiheader & 3
                #print(f"foud dofus packet, hiheader: {hiheader}, packetId: {packetId}, lengthType: {lengthType}")
                dofus_packet = DofusPacket(payload)
                dofus_packet.direction = direction
                #print("------------------------------")
                #print(dofus_packet)
                #print("------------------------------")

try:
    #sniff(filter="tcp port 5555", prn=packetcallback)
    sniff(filter="tcp port 5555", prn=newCallback)
except:
    print("Sorry, can\'t read network traffic. Are you root?")
