import importlib
import os
import pathlib
import re

import pyshark
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


def packetcallback(raw_packet):
    # print("received a packet")
    # print(raw_packet.summary())
    if "TCP" in raw_packet:
        # print("le packet a TCP")
        # print(raw_packet["TCP"].sport)
        direction = None
        if raw_packet["TCP"].sport == 5555:
            direction = "from_client"
        if raw_packet["TCP"].dport == 5555:
            direction = "to_client"
        if direction is not None:
            # payload = getattr(raw_packet.tcp, 'payload', None)
            # payload = getattr(raw_packet.tcp, 'data', None)
            payload = None
            try:
                #print("raw_packet: ", bytes(raw_packet["TCP"].payload))
                payload = bytes(raw_packet["TCP"].payload)

                # print(raw_packet.data.data)
                # payload = raw_packet.data.data
            except:
                print("no data")
            if payload:
                try:
                    # dofus_packet = DofusPacket(bytes.fromhex(payload.replace(':', '')))
                    dofus_packet = DofusPacket(payload)
                    dofus_packet.direction = direction
                    print("------------------------------")
                    print(dofus_packet)
                    print("------------------------------")
                    if dofus_packet.message_type == "MapInformationsRequestMessage":
                        mapInfo = MapInformationsRequestMessage(dofus_packet.hexContent)
                        print(f"mapInfo: {mapInfo.mapId}")
                except Exception as e:
                    print("opusie un bug")
                    print(e)
                    print("------------------------------")
            # else:
            #     print("------------------------------")
            #     print("TCP layer has no payload.")
            #     print("------------------------------")





try:
    sniff(filter="tcp port 5555", prn=packetcallback)
except:
    print("Sorry, can\'t read network traffic. Are you root?")
