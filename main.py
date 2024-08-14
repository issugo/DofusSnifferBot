import os
import pyshark
import struct

from HexReader import HexReader

ethernetNicUUID = '\\Device\\NPF_{AC96C4C9-D4B2-4ABD-A5FC-8F5BC32BF1F0}'
correspondence = {}

if not os.path.isfile("correspondance.txt"):
    with open("utils/findIds.py") as file:
        exec(file.read())

if os.stat("correspondance.txt").st_size == 0:
    with open("utils/findIds.py") as file:
        exec(file.read())


def load_correspondence(file_path):
    with open(file_path, 'r') as file_correspondence:
        for line in file_correspondence:
            class_name, message_id = line.strip().split(':')
            correspondence[int(message_id)] = class_name
    return correspondence


def deserialize_as_map_complementary_informations_with_coords_message(hexInput):
    reader = HexReader(hexInput)

    worlX = reader.read_short_big_endian()
    worlY = reader.read_short_big_endian()
    print(f"map coord: {worlX}:{worlY}")

def deserialize_as_map_complementary_informations_data_message(hexInput, direction):
    reader = HexReader(hexInput)

    if direction == "from_client":
        reader.set_cursor_position(4)

    areaId = reader.read_short_big_endian()
    if areaId < 0:
        print(f"ERROR !!!! areaId {areaId} incorrect")
        return
    print(f"areaId: {areaId}")
    mapId = reader.read_bdouble()
    #if mapId < 0 or mapId > 9007199254740992:
    #    print(f"ERROR !!!! mapId {mapId} incorrect")
    #    return
    print(f"mapId: {mapId}")

    houses_len = reader.read_short_big_endian()
    print(f"read houses_len: {houses_len}")
    for _ in range(houses_len):
        id3 = reader.read_short_big_endian()
        #item3 = ProtocolTypeManager.get_instance(HouseInformations, id3)
        #item3.deserialize(input)
        #self.houses.append(item3)

    actors_len = reader.read_short_big_endian()
    print(f"read actors_len: {actors_len}")
    for _ in range(actors_len):
        id4 = reader.read_short_big_endian()
        #item4 = ProtocolTypeManager.get_instance(GameRolePlayActorInformations, id4)
        #item4.deserialize(input)
        #self.actors.append(item4)

    interactive_elements_len = reader.read_short_big_endian()
    print(f"read interactive_elements_len: {interactive_elements_len}")
    for _ in range(interactive_elements_len):
        id5 = reader.read_short_big_endian()
        print(f"found interactive element of id {id5}")
        # item5 = ProtocolTypeManager.get_instance(InteractiveElement, id5)
        # item5.deserialize(input)
        # self.interactive_elements.append(item5)

    # stated_elements_len = reader.read_short_big_endian()
    # for _ in range(stated_elements_len):
    #     item6 = StatedElement()
    #     item6.deserialize(input)
    #     self.stated_elements.append(item6)

    # obstacles_len = reader.read_short_big_endian()
    # for _ in range(obstacles_len):
    #     item7 = MapObstacle()
    #     item7.deserialize(input)
    #     self.obstacles.append(item7)

    # fights_len = reader.read_short_big_endian()
    # for _ in range(fights_len):
    #     item8 = FightCommonInformations()
    #     item8.deserialize(input)
    #     self.fights.append(item8)

    has_aggressive_monsters = reader.read_boolean()
    #self.fight_start_positions = FightStartingPositions()
    #self.fight_start_positions.deserialize(input)






try:
    load_correspondence("correspondance.txt")
    capture = pyshark.LiveCapture(interface=ethernetNicUUID)
    for raw_packet in capture.sniff_continuously():
        #print(raw_packet)
        if hasattr(raw_packet, 'tcp'):
            if raw_packet.tcp.srcport == '5555' or raw_packet.tcp.dstport == '5555':
                direction = "from_client" if raw_packet.tcp.dstport == '5555' else "to_client"
                payload = getattr(raw_packet.tcp, 'payload', None)
                if payload:
                    try:
                        dofus_data = bytes.fromhex(payload.replace(':', ''))
                        parsed_packet = parse_dofus_packet(dofus_data)
                        if parsed_packet:
                            # print(f"Dofus Packet: {parsed_packet}")
                            if parsed_packet['message_type'] == "MapComplementaryInformationsDataMessage":
                                print(f"packet length: {parsed_packet['length']}")
                                print(f"packet id: {parsed_packet['packet_id']}")
                                try:
                                    deserialize_as_map_complementary_informations_data_message(parsed_packet['content'], direction)
                                except EOFError as e:
                                    print(f"EOFError: {e}")
                            if parsed_packet['message_type'] == "MapComplementaryInformationsWithCoordsMessage":
                                print(f"packet length: {parsed_packet['length']}")
                                print(f"packet id: {parsed_packet['packet_id']}")
                                try:
                                    deserialize_as_map_complementary_informations_with_coords_message(parsed_packet['content'])
                                except EOFError as e:
                                    print(f"EOFError: {e}")
                    except ValueError as e:
                        print(f"Failed to parse TCP payload: {payload} - {e}")
                else:
                    print("TCP layer has no payload.")
except KeyboardInterrupt:
    print(capture)



