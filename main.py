import importlib
import os
import pathlib
import re

import pyshark

from ankama.DofusPacket import DofusPacket


ethernetNicUUID = '\\Device\\NPF_{AC96C4C9-D4B2-4ABD-A5FC-8F5BC32BF1F0}'

if not os.path.isfile("correspondance.txt"):
    with open("utils/findIds.py") as file:
        exec(file.read())

if os.stat("correspondance.txt").st_size == 0:
    with open("utils/findIds.py") as file:
        exec(file.read())

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

try:
    capture = pyshark.LiveCapture(interface=ethernetNicUUID)
    for raw_packet in capture.sniff_continuously():
        if hasattr(raw_packet, 'tcp'):
            direction = None
            if raw_packet.tcp.srcport == '5555':
                direction = "from_client"
            if raw_packet.tcp.dstport == '5555':
                direction = "to_client"
            if direction is not None:
                payload = getattr(raw_packet.tcp, 'payload', None)
                if payload:
                    dofus_packet = DofusPacket(bytes.fromhex(payload.replace(':', '')))
                    print(dofus_packet)
                else:
                    print("TCP layer has no payload.")
except KeyboardInterrupt:
    print(capture)
