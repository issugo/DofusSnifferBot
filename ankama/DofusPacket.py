import json
import struct


class DofusPacket:
    # dofus packet hi_header
    hi_header = ''
    # dofus packet id
    packet_id = 0
    # associated message type
    message_type = ''
    # length of payload
    length = 0
    # raw length
    raw_length = ''
    # raw payload
    content = ''
    # hex content
    hexContent = b''
    # type of content length
    length_type = 0
    # correspondence between mesage ids and message type
    correspondence = {}
    # direction should to_client, from_client or None
    direction = None

    def __str__(self):
        return f"packet_id: {self.packet_id}, direction: {self.direction}, message_type: {self.message_type}, lenght: {self.length}, content: {self.content}, raw_length: {self.raw_length.hex()}, hi_header: {self.hi_header.hex()}"

    def __init__(self, packet):
        with open("IdToMessage.json", "r") as correspondenceJsonFile:
            self.correspondence = json.load(correspondenceJsonFile)
        # find and decode hi_header
        raw_hi_header = packet[:2]
        self.hi_header = raw_hi_header
        # print("raw_hi_deader: ", bytes.hex(raw_hi_header))
        self.packet_id, self.length_type = DofusPacket.decode_hi_header(raw_hi_header)
        self.message_type = self.correspondence[str(self.packet_id)]

        # find and decode length
        length_bytes = packet[2:2 + self.length_type]
        self.raw_length = length_bytes
        self.length = DofusPacket.decode_length(length_bytes, self.length_type)

        # set content
        self.content = packet[2 + self.length_type:2 + self.length_type + self.length]
        # print("content: ", bytes.hex(self.content))
        self.hexContent = self.content.hex()

    @staticmethod
    def decode_hi_header(raw_hi_header):
        hiheader = int.from_bytes(raw_hi_header, byteorder='big', signed=False)
        packet_id = hiheader >> 2
        length_type = hiheader & 3
        return packet_id, length_type

    @staticmethod
    def decode_length(data, length_type):
        if length_type == 0:
            return 0
        elif length_type == 1:
            # return struct.unpack('>B', data[:1])[0]
            return int.from_bytes(data[:1], byteorder='big', signed=False)
        elif length_type == 2:
            # return struct.unpack('>H', data[:2])[0]
            return int.from_bytes(data[:2], byteorder='big', signed=False)
        elif length_type == 3:
            # return struct.unpack('>I', b'\x00' + data[:3])[0]
            return int.from_bytes(data[:3], byteorder='big', signed=False)

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
