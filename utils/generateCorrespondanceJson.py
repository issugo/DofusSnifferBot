import json

correspondence = {}


def load_correspondence(file_path):
    with open(file_path, 'r') as file_correspondence:
        for line in file_correspondence:
            class_name, message_id = line.strip().split(':')
            correspondence[class_name] = str(int(message_id))
            correspondence[str(int(message_id))] = class_name
    return correspondence


load_correspondence("../correspondance.txt")
with open("../IdToMessage.json", "w") as idToMessageFile:
    idToMessageFile.write(
        json.dumps(correspondence, indent=4, sort_keys=True)
    )
