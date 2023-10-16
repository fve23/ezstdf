from .StdfReaderBase import StdfReaderBase
import io
import pandas as pd
from .stdf_cst import StdfRecordType, stdf_record_fields, stdf_record_parsers
from .atdf_cst import atdf_record_fields
import re
from datetime import datetime
from .parsers import ParserDataByRef


"""
Copyright (c) 2023 fve23

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class StdfRecord:
    # -- This is a list of record types that are supported --
    # not sure: gdr
    # parsable_record_types = (
    #     "far", "atr", "mir", "mrr", "pcr", "hbr", "sbr", "pmr", "sdr", "wir", "wrr", "wcr",
    #     "pir", "prr", "tsr", "ptr", "bps", "eps", "dtr", "ftr", "mpr"
    # )
    parsable_record_types = None  # None -> parse all record types
    prog_date = re.compile(r"[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2} [0-9]{1,2}-[a-zA-Z]{3}-[0-9]{2,4}")
    prog_float = re.compile(r"[-+]?([0-9]*[.])?[0-9]+([eE][-+]?\d+)?")

    def __init__(self, rec_typ: int, rec_sub: int, is_atdf=False):
        self.rec_typ = rec_typ
        self.rec_sub = rec_sub
        self.rec_pair = (rec_typ, rec_sub)
        self._temp_rows = []
        self.parsers = None
        self.is_atdf = is_atdf
        try:
            rec_cst = StdfRecordType(self.rec_pair)
            if is_atdf:
                fields = atdf_record_fields.get(rec_cst)
            else:
                fields = stdf_record_fields.get(rec_cst)
            if self.parsable_record_types is None or rec_cst.name in self.parsable_record_types:
                self.parsers = stdf_record_parsers.get(rec_cst)
        except ValueError:
            fields = None
        self.df = pd.DataFrame(columns=fields)

    def parse_data(self, data: io.BytesIO, byte_order, data_by_ref: ParserDataByRef):
        if self.parsers:
            values = []
            prev_value = None
            latest_valid_int = None
            for f in self.parsers:
                prev_value = f(data, byte_order, prev_value, data_by_ref)
                values.append(prev_value)
            self._temp_rows.append(values)

    def parse_data_str(self, data: str, separator: str):
        values = data.split(separator)
        values = [x.strip() for x in values]
        current_len = len(values)
        if current_len == 1 and not values[0]:
            # avoid issue with eps record
            return
        # parse dates and floats
        for n, temp in enumerate(values):
            match = self.prog_date.match(temp)
            if match:
                try:
                    date = datetime.strptime(temp, '%H:%M:%S %d-%b-%Y')
                    values[n] = date
                    continue
                except ValueError:
                    # invalid date string, just ignore
                    continue
            if self.prog_float.match(temp):
                try:
                    values[n] = float(temp)
                    continue
                except ValueError:
                    continue

        # save data
        expected_len = len(self.df.columns)
        if current_len < expected_len:
            values += [None] * (expected_len - current_len)
        self._temp_rows.append(values)

    def parse_generic_type(self, data: str):
        data_type = data[0]
        data = data[1:]
        if data_type == "T":
            return data
        if data_type in ("M", "U", "B", "I", "S", "L", "N"):
            return int(data, 10)
        if data_type in ("F", "D"):
            return float(data)
        if data_type in ("X", "Y"):
            temp = []
            while data:
                temp.append(int(data[:2], 16))
                data = data[2:]
            return temp

    def finalize(self):
        """
        All the rows have been parsed, time to create a dataframe
        :return:
        """
        if not self._temp_rows:
            return
        columns = self.df.columns
        if self.is_atdf and self.rec_pair == StdfRecordType.gdr.value:
            # special case for generic data record
            new_rows = []
            for row in self._temp_rows:
                for item in row:
                    new_rows.append(self.parse_generic_type(item))
            self._temp_rows = new_rows
        # TODO data scaling
        if self.rec_pair == StdfRecordType.ptr.value:
            # The first PTR for each test will have these fields filled in. The values in these fields will be the
            # default values for each subsequent PTR with the same test number. If the field is filled in for
            # subsequent PTRs, that value will override the default. Otherwise the default will be used.
            # TODO propagate PTR from first row
            pass
        try:
            self.df = pd.DataFrame(self._temp_rows, columns=columns)
        except ValueError as e:
            # print(f"Incompatible number of columns: {len(self._temp_rows[0])}, expected={len(columns)}")
            # print(f"Record type was: {self.rec_pair}")
            raise e
        self._temp_rows = None


class StdfReader(StdfReaderBase):
    def parse_file(self, path):
        stream = io.FileIO(path, mode="rb")
        data = stream.read(5)
        stream.seek(0)
        if data[4] == ord('A'):
            self.parse_atdf(stream)
        else:
            self.parse_stdf(stream)
        stream.close()

    def parse_stdf(self, stream: io.IOBase):
        """
        Parse a binary STDF file and append the records to the existing ones (if any).
        :param stream: an IO stream opened in binary mode
        :return:
        """
        # -- Detect the endianness --
        if self.byte_order == "auto":
            temp = stream.read(1)
            if temp[0] == 0:
                # the first record has always a size of 2
                byte_order = "big"
            else:
                byte_order = "little"
        else:
            byte_order = self.byte_order
        stream.seek(0)
        # -- Parse all the records --
        data_by_ref = ParserDataByRef()
        while True:
            temp = stream.read(2)
            if b'' == temp:
                # EOF
                break
            # get the record type and subtype
            rec_len = int.from_bytes(temp, byte_order)
            rec_typ = stream.read(1)[0]
            rec_sub = stream.read(1)[0]
            record_data = stream.read(rec_len)
            # parse the record
            record = self.records.get((rec_typ, rec_sub), None)
            if record is None:
                # create a new empty record
                record = StdfRecord(rec_typ, rec_sub)
                self.records[(rec_typ, rec_sub)] = record
            record.parse_data(io.BytesIO(record_data), byte_order, data_by_ref)
        for rec in self.records.values():
            rec.finalize()

    @staticmethod
    def __rec_cst_for_name(name: str):
        """
        Convenience method that converts a string into a StdfRecordType enum
        :param name: the name of the record type, e.g "MIR" etc.
        :return:
        """
        name = name.lower()
        for rec in StdfRecordType:
            if rec.name == name:
                return rec

    def __parse_line(self, line, separator, data_by_ref: ParserDataByRef):
        if not line:
            return
        rec_type = line[:3]
        rec_cst = self.__rec_cst_for_name(rec_type)
        assert rec_cst is not None, f"Unknown record type {rec_type}, line: {line}"
        # parse the record
        line = line[4:]
        record = self.records.get(rec_cst.value, None)
        if record is None:
            record = StdfRecord(*rec_cst.value, is_atdf=True)
            self.records[rec_cst.value] = record
        record.parse_data_str(line, separator)

    def parse_atdf(self, stream: io.IOBase):
        """
        Parse a clear text ATDF file and append the records to the existing ones (if any).
        :param stream: an IO stream opened in binary mode
        :return:
        """
        separator = None
        current_record = None
        data_by_ref = ParserDataByRef()
        while True:
            line = stream.readline()
            if not line:
                # EOF
                break
            line = line.decode("utf-8", "ignore")
            if separator is None:
                assert len(line) > 6, "Invalid FAR"
                separator = line[5]  # This separator is the sixth character in the file
            line = line.replace("\n", "").replace("\r", "")
            if not line:
                continue
            if line[0] == " ":
                # line continuation
                current_record += line
            elif line[3] == ":":
                self.__parse_line(current_record, separator, data_by_ref)
                current_record = line
            else:
                raise Exception(f"Invalid line {line}")
        if current_record:
            self.__parse_line(current_record, separator, data_by_ref)
        for rec in self.records.values():
            rec.finalize()
