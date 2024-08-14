import os
import pathlib
import re

MESSAGE_FOLDER = pathlib.Path('C:/Program Files (x86)/FFDec/scripts/com/ankamagames/dofus/network/messages')

with open("correspondance.txt", "w") as correspondanceFile:
    for root, dirs, files in os.walk(MESSAGE_FOLDER):
        for file in files:
            filePath = pathlib.Path(root, file)
            with open(filePath, 'r') as file_open:
                asClassFileLines = file_open.readlines()
                # print(asClassFileLines)
                for line in asClassFileLines:
                    if re.match(r".*protocolId:uint.*", line):
                        messageId = re.search(r"\d+", line)
                        print(f"class {file.split('.')[0]} has message id {messageId.group()}")
                        correspondanceFile.write(f"{file.split('.')[0]}:{messageId.group()}\n")
