import json
import struct


class DofusPacket:
    # dofus packet id
    packet_id = 0
    # associated message type
    message_type = ''
    # length of payload
    length = 0
    # raw payload
    content = ''
    # hex content
    hexContent = b''
    # type of content length
    length_type = 0
    # correspondence between mesage ids and message type
    correspondence = {}

    def __init__(self, packet):
        with open("IdToMessage.json", "r") as correspondenceJsonFile:
            self.correspondence = json.load(correspondenceJsonFile)
        # find and decode hi_header
        hi_header = packet[:2]
        self.packet_id, self.length_type = DofusPacket.decode_hi_header(hi_header)

        # find and decode length
        length_bytes = packet[2:2 + self.length_type]
        self.length = DofusPacket.decode_length(length_bytes, self.length_type)

        # set content
        self.content = packet[2 + self.length_type:2 + self.length_type + self.length]
        self.hexContent = self.content.hex()

    @staticmethod
    def decode_hi_header(hi_header):
        hi_header = struct.unpack('>H', hi_header)[0]
        packet_id = hi_header >> 2
        length_type = hi_header & 3
        return packet_id, length_type

    @staticmethod
    def decode_length(data, length_type):
        if length_type == 0:
            return 0
        elif length_type == 1:
            return struct.unpack('>B', data[:1])[0]
        elif length_type == 2:
            return struct.unpack('>H', data[:2])[0]
        elif length_type == 3:
            return struct.unpack('>I', b'\x00' + data[:3])[0]

    @staticmethod
    def parse_dofus_packet(raw_packet, correspondence):
        if len(raw_packet) < 2:
            return None

        hi_header = raw_packet[:2]
        packet_id, length_type = DofusPacket.decode_hi_header(hi_header)

        length_bytes = raw_packet[2:2 + length_type]
        length = DofusPacket.decode_length(length_bytes, length_type)

        content = raw_packet[2 + length_type:2 + length_type + length]

        return {
            'packet_id': packet_id,
            'message_type': correspondence.get(packet_id, 'Unknown'),
            'length': length,
            'content': content.hex()
        }
