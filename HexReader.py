import struct


class HexReader:
    def __init__(self, hex_string, cursor: int = 0):
        self.data = bytes.fromhex(hex_string)
        self.cursor = cursor

    def read_unsigned_short_big_endian(self):
        if self.cursor + 2 > len(self.data):
            raise EOFError("Not enough data to read a short")

        # Read 2 bytes and unpack as big-endian unsigned short
        # short_value = struct.unpack('>H', self.data[self.cursor:self.cursor + 2])[0]
        short_value = int.from_bytes(self.data[:2], byteorder='big', signed=False)
        self.cursor += 2
        # print("DEBUG short!!!!!", self.data[self.cursor:])
        return short_value

    def read_signed_short_big_endian(self):
        if self.cursor + 2 > len(self.data):
            raise EOFError("Not enough data to read a short")
        short_value = int.from_bytes(self.data[:2], byteorder='big', signed=True)
        self.cursor += 2
        return short_value

    def read_boolean(self):
        if self.cursor + 1 > len(self.data):
            raise EOFError("Not enough data to read a boolean")

        # boolean_value = self.data[self.cursor] != 0
        boolean_value = bool.from_bytes(bytes(self.data[self.cursor]), byteorder='big', signed=True)
        self.cursor += 1
        # print("DEBUG bool!!!!!", self.data[self.cursor:])
        return boolean_value

    def read_unsigned_int_big_endian(self):
        if self.cursor + 4 > len(self.data):
            raise EOFError("Not enough data to read a bdouble")

        # Read 8 bytes and unpack as big-endian double
        # double_value = struct.unpack('>d', self.data[self.cursor:self.cursor + 8])[0]
        double_value = int.from_bytes(self.data[self.cursor:self.cursor + 4], byteorder='big', signed=False)
        self.cursor += 4
        return double_value

    def read_signed_int_big_endian(self):
        if self.cursor + 4 > len(self.data):
            raise EOFError("Not enough data to read a bdouble")

        # Read 8 bytes and unpack as big-endian double
        # double_value = struct.unpack('>d', self.data[self.cursor:self.cursor + 8])[0]
        double_value = int.from_bytes(self.data[self.cursor:self.cursor + 4], byteorder='big', signed=True)
        self.cursor += 4
        return double_value

    def read_unsigned_double_big_endian(self):
        if self.cursor + 8 > len(self.data):
            raise EOFError("Not enough data to read a bdouble")

        # Read 8 bytes and unpack as big-endian double
        # double_value = struct.unpack('>d', self.data[self.cursor:self.cursor + 8])[0]
        double_value = int.from_bytes(self.data[self.cursor:self.cursor + 8], byteorder='big', signed=False)
        self.cursor += 8
        return double_value

    def read_signed_double_big_endian(self):
        if self.cursor + 8 > len(self.data):
            raise EOFError("Not enough data to read a bdouble")

        # Read 8 bytes and unpack as big-endian double
        # double_value = struct.unpack('>d', self.data[self.cursor:self.cursor + 8])[0]
        double_value = int.from_bytes(self.data[self.cursor:self.cursor + 8], byteorder='big', signed=True)
        self.cursor += 8
        return double_value

    def get_cursor_position(self):
        return self.cursor

    def set_cursor_position(self, position):
        if position < 0 or position > len(self.data):
            raise ValueError("Invalid cursor position")
        self.cursor = position
