import struct

from HexReader import HexReader


class MapInformationsRequestMessage:
    # protocolId is the network packet id of the message
    protocolId = 2408

    # ALL DATA FROM PACKET
    # double
    mapId = 0

    def __init__(self, dataInput):
        """
        dataInput should be binary data
        the init should construct the data in the same way as the dofus original code
        """
        reader = HexReader(dataInput)
        self.mapId = reader.read_bdouble()

    @staticmethod
    def serializeAsMapInformationsRequestMessage(dataInput):
        """
        dataInput should be of type MapInformationsRequestMessage
        """
        buffer = bytearray()
        buffer.extend(struct.pack('>d', dataInput.mapId))
        return buffer

    @staticmethod
    def deserializeAsMapInformationsRequestMessage(dataInput):
        """
        dataInput should be bynary data
        """
        return MapInformationsRequestMessage(dataInput)
