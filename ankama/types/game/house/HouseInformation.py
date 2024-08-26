from HexReader import HexReader


class HouseInformation:

    houseId = 0
    modelId = 0

    def __init__(self, dataInput, *args, readerCursor: int = -1):
        reader = None
        if readerCursor >= -1:
            reader = HexReader(dataInput, readerCursor)
        else:
            reader = HexReader(dataInput)
        houseId = reader.read_unsigned_int_big_endian()
        modelId = reader.read_unsigned_short_big_endian()
        if houseId < 0:
            raise ValueError("houseId negative")
        if modelId < 0:
            raise ValueError("modelId negative")

    @staticmethod
    def deserializeAsHouseInformation(dataInput):
        return HouseInformation(dataInput)
