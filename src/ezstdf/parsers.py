import datetime
import math
import struct


def parse_str(data, byte_order, prev_value):
    temp = data.read(1)
    if temp == b'':
        return None
    temp = data.read(temp[0])
    return temp.decode("utf-8", "ignore")


def parse_str_array(data, byte_order, prev_value):
    temp = []
    for _ in range(prev_value):
        temp.append(parse_str(data, byte_order, prev_value))
    return temp


def parse_float(data, byte_order, prev_value):
    x = data.read(4)
    if len(x) == 4:
        if byte_order == "big":
            return struct.unpack('>f', x)[0]
        return struct.unpack('<f', x)[0]
    return None


def parse_double(data, byte_order, prev_value):
    x = data.read(8)
    if len(x) == 8:
        if byte_order == "big":
            return struct.unpack('>d', x)[0]
        return struct.unpack('<d', x)[0]
    return None


def parse_u32(data, byte_order, prev_value):
    return int.from_bytes(data.read(4), byte_order)


def parse_u16(data, byte_order, prev_value):
    return int.from_bytes(data.read(2), byte_order)


def parse_u16_array(data, byte_order, prev_value):
    temp = []
    for _ in range(prev_value):
        temp.append(int.from_bytes(data.read(2), byte_order))
    return temp


def parse_i16(data, byte_order, prev_value):
    x = data.read(2)
    if len(x) == 2:
        if byte_order == "big":
            return struct.unpack('>h', x)[0]
        return struct.unpack('<h', x)[0]
    return None


def parse_i8(data, byte_order, prev_value):
    x = data.read(1)
    if b'' == x:
        return None
    return struct.unpack('b', x)[0]


def parse_u8(data, byte_order, prev_value):
    x = data.read(1)
    if b'' == x:
        return None
    return x[0]


def parse_u8_array(data, byte_order, prev_value):
    temp = []
    length = data.read(1)[0]
    for _ in range(length):
        temp.append(int.from_bytes(data.read(1), byte_order))
    return temp


def parse_date(data, byte_order, prev_value):
    u = parse_u32(data, byte_order, prev_value)
    return datetime.datetime.fromtimestamp(u)


def parse_char(data, byte_order, prev_value):
    return data.read(1).decode('utf-8', 'ignore')


def parse_i32(data, byte_order, prev_value):
    x = data.read(4)
    if len(x) == 4:
        if byte_order == "big":
            return struct.unpack('>i', x)[0]
        return struct.unpack('<i', x)[0]
    return None


def parse_bit_fields(data, byte_order, prev_value):
    length = parse_u32(data, byte_order, prev_value)
    num_bytes = int(math.ceil(length / 8))
    raw = data.read(num_bytes)
    return [x[0] for x in raw]


def parse_variable_field(data, byte_order, prev_value):
    generic_data = []
    for _ in range(prev_value):
        data_type = data.read(1)[0]
        if data_type == 0:
            continue
        elif data_type == 1:
            generic_data.append(parse_u8(data, byte_order, prev_value))
        elif data_type == 2:
            generic_data.append(parse_u16(data, byte_order, prev_value))
        elif data_type == 3:
            generic_data.append(parse_u32(data, byte_order, prev_value))
        elif data_type == 4:
            generic_data.append(parse_i8(data, byte_order, prev_value))
        elif data_type == 5:
            generic_data.append(parse_i16(data, byte_order, prev_value))
        elif data_type == 6:
            generic_data.append(parse_i32(data, byte_order, prev_value))
        elif data_type == 7:
            generic_data.append(parse_float(data, byte_order, prev_value))
        elif data_type == 8:
            generic_data.append(parse_double(data, byte_order, prev_value))
        elif data_type == 10:
            generic_data.append(parse_str(data, byte_order, prev_value))
        elif data_type == 11:
            generic_data.append(parse_u8_array(data, byte_order, data.read(1)[0]))
        elif data_type == 12:
            generic_data.append(parse_u8_array(data, byte_order, parse_u16(data, byte_order, None)))
        elif data_type == 13:
            generic_data.append(parse_u8(data, byte_order, prev_value))
