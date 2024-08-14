import os
import pathlib

MESSAGE_FOLDER = pathlib.Path("ankama/messages")

for root, dirs, files in os.walk(MESSAGE_FOLDER):
    for file in files:
        print(f"treating file: {file}")
        classFilePath = pathlib.Path(root, file)
        with open(classFilePath, "w") as classFile:
            if file != "__init__.py":
                classFile.write(f'class {file[:-3]}:\n\tdef __init__(self):\n\t\traise NotImplementedError("class {file[:-3]} not yet implemented")\n')
