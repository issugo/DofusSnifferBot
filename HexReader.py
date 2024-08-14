import struct


class HexReader:
    def __init__(self, hex_string):
        self.data = bytes.fromhex(hex_string)
        self.cursor = 0

    def read_short_big_endian(self):
        if self.cursor + 2 > len(self.data):
            raise EOFError("Not enough data to read a short")

        # Read 2 bytes and unpack as big-endian unsigned short
        short_value = struct.unpack('>H', self.data[self.cursor:self.cursor + 2])[0]
        self.cursor += 2
        # print("DEBUG short!!!!!", self.data[self.cursor:])
        return short_value

    def read_boolean(self):
        if self.cursor + 1 > len(self.data):
            raise EOFError("Not enough data to read a boolean")

        boolean_value = self.data[self.cursor] != 0
        self.cursor += 1
        # print("DEBUG bool!!!!!", self.data[self.cursor:])
        return boolean_value

    def read_bdouble(self):
        if self.cursor + 8 > len(self.data):
            raise EOFError("Not enough data to read a bdouble")

        # Read 8 bytes and unpack as big-endian double
        double_value = struct.unpack('>d', self.data[self.cursor:self.cursor + 8])[0]
        # print(f"binary string: {self.data[self.cursor:self.cursor + 8]}")
        # print(f"Int value: {self.data[self.cursor:self.cursor + 8].decode()}")
        self.cursor += 8
        # print("DEBUG double!!!!!", self.data[self.cursor:])
        return double_value

    def get_cursor_position(self):
        return self.cursor

    def set_cursor_position(self, position):
        if position < 0 or position > len(self.data):
            raise ValueError("Invalid cursor position")
        self.cursor = position
