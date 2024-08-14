from HexReader import HexReader


class MapInformationsRequestMessage:
    # protocolId is the network packet id of the message
    protocolId = 2408

    # ALL DATA FROM PACKET
    # double
    mapId = 0

    def __init__(self, dataInput):
        reader = HexReader(dataInput)
        self.mapId = reader.read_bdouble()
        raise NotImplementedError("class MapInformationsRequestMessage not yet implemented")

    @staticmethod
    def serializeAsMapInformationsRequestMessage(dataInput):
        raise NotImplementedError("class MapInformationsRequestMessage not yet implemented")

    @staticmethod
    def deserializeAsMapInformationsRequestMessage(dataInput):
        return MapInformationsRequestMessage(dataInput)
