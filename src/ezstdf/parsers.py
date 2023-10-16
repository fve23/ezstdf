import datetime
import math
import struct


class ParserDataByRef:
    def __init__(self):
        self.latest_valid_unsigned = None
        self.previous_valid_unsigned = None


def parse_str(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = data.read(1)
    if temp == b'':
        return None
    temp = data.read(temp[0])
    temp = temp.decode("utf-8", "ignore")
    temp = temp.replace('\x00', '')
    return temp


def parse_str_array(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    for _ in range(prev_value):
        temp.append(parse_str(data, byte_order, prev_value, data_by_ref))
    return temp


def parse_str_array_kx(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    for _ in range(data_by_ref.latest_valid_unsigned):
        temp.append(parse_str(data, byte_order, prev_value, data_by_ref))
    return temp


def parse_float(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    x = data.read(4)
    if len(x) == 4:
        if byte_order == "big":
            return struct.unpack('>f', x)[0]
        return struct.unpack('<f', x)[0]
    return None


def parse_double(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    x = data.read(8)
    if len(x) == 8:
        if byte_order == "big":
            return struct.unpack('>d', x)[0]
        return struct.unpack('<d', x)[0]
    return None


def parse_u32(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    return int.from_bytes(data.read(4), byte_order)


def parse_u16(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    x = int.from_bytes(data.read(2), byte_order)
    data_by_ref.previous_valid_unsigned = data_by_ref.latest_valid_unsigned
    data_by_ref.latest_valid_unsigned = x
    return x


def parse_u16_array(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    for _ in range(prev_value):
        temp.append(int.from_bytes(data.read(2), byte_order))
    return temp


def parse_u16_array_kx(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    for _ in range(data_by_ref.latest_valid_unsigned):
        temp.append(int.from_bytes(data.read(2), byte_order))
    return temp


def parse_u16_array_jx(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    for _ in range(data_by_ref.previous_valid_unsigned):
        temp.append(int.from_bytes(data.read(2), byte_order))
    return temp


def parse_i16(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    x = data.read(2)
    if len(x) == 2:
        if byte_order == "big":
            return struct.unpack('>h', x)[0]
        return struct.unpack('<h', x)[0]
    return None


def parse_i8(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    x = data.read(1)
    if b'' == x:
        return None
    return struct.unpack('b', x)[0]


def parse_u8(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    x = data.read(1)
    if b'' == x:
        return None
    x = x[0]
    data_by_ref.previous_valid_unsigned = data_by_ref.latest_valid_unsigned
    data_by_ref.latest_valid_unsigned = x
    return x


def parse_u8_array(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    length = data.read(1)[0]
    for _ in range(length):
        temp.append(data.read(1)[0])
    return temp


def parse_u8_array_kx(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    length = data_by_ref.latest_valid_unsigned
    for _ in range(length):
        temp.append(data.read(1)[0])
    return temp


def parse_u8_array_jx(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    temp = []
    length = data_by_ref.previous_valid_unsigned
    for _ in range(length):
        temp.append(data.read(1)[0])
    return temp


def parse_date(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    u = parse_u32(data, byte_order, prev_value, data_by_ref)
    return datetime.datetime.fromtimestamp(u)


def parse_char(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    return data.read(1).decode('utf-8', 'ignore')


def parse_i32(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    x = data.read(4)
    if len(x) == 4:
        if byte_order == "big":
            return struct.unpack('>i', x)[0]
        return struct.unpack('<i', x)[0]
    return None


def parse_bit_fields(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    length = parse_u32(data, byte_order, prev_value, data_by_ref)
    num_bytes = int(math.ceil(length / 8))
    raw = data.read(num_bytes)
    return [x[0] for x in raw]


def parse_variable_field(data, byte_order, prev_value, data_by_ref: ParserDataByRef):
    generic_data = []
    for _ in range(prev_value):
        data_type = data.read(1)[0]
        if data_type == 0:
            continue
        elif data_type == 1:
            generic_data.append(parse_u8(data, byte_order, prev_value, data_by_ref))
        elif data_type == 2:
            generic_data.append(parse_u16(data, byte_order, prev_value, data_by_ref))
        elif data_type == 3:
            generic_data.append(parse_u32(data, byte_order, prev_value, data_by_ref))
        elif data_type == 4:
            generic_data.append(parse_i8(data, byte_order, prev_value, data_by_ref))
        elif data_type == 5:
            generic_data.append(parse_i16(data, byte_order, prev_value, data_by_ref))
        elif data_type == 6:
            generic_data.append(parse_i32(data, byte_order, prev_value, data_by_ref))
        elif data_type == 7:
            generic_data.append(parse_float(data, byte_order, prev_value, data_by_ref))
        elif data_type == 8:
            generic_data.append(parse_double(data, byte_order, prev_value, data_by_ref))
        elif data_type == 10:
            generic_data.append(parse_str(data, byte_order, prev_value, data_by_ref))
        elif data_type == 11:
            generic_data.append(parse_u8_array(data, byte_order, data.read(1)[0], data_by_ref))
        elif data_type == 12:
            generic_data.append(
                parse_u8_array(data, byte_order, parse_u16(data, byte_order, None, data_by_ref), data_by_ref)
            )
        elif data_type == 13:
            generic_data.append(parse_u8(data, byte_order, prev_value, data_by_ref))
