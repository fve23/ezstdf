import pandas as pd
from .stdf_cst import StdfRecordType

"""
This base class contains properties to directly access all the records
"""


class StdfReaderBase:
    def __init__(self, byte_order="auto"):
        self.byte_order = byte_order
        self.records = {}

    def get_record(self, rec_cst: StdfRecordType) -> pd.DataFrame:
        record = self.records.get(rec_cst.value)
        if record is not None:
            return record.df
        return None

    def get_total_record_count(self):
        count = 0
        for rec in self.records.values():
            count += len(rec.df)
        return count

    def to_excel(self, path, engine=None):
        with pd.ExcelWriter(path, engine=engine) as writer:
            for k, v in self.records.items():
                rec_cst = StdfRecordType(k)
                v.df.to_excel(writer, sheet_name=rec_cst.name)

    @property
    def pir(self) -> pd.DataFrame:
        # Part Information Record
        return self.get_record(StdfRecordType.pir)

    @property
    def gdr(self) -> pd.DataFrame:
        # Generic Data Record
        return self.get_record(StdfRecordType.gdr)

    @property
    def mrr(self) -> pd.DataFrame:
        # Master Results Record
        return self.get_record(StdfRecordType.mrr)

    @property
    def pgr(self) -> pd.DataFrame:
        # Pin Group Record
        return self.get_record(StdfRecordType.pgr)

    @property
    def sdr(self) -> pd.DataFrame:
        # Site Description Record
        return self.get_record(StdfRecordType.sdr)

    @property
    def bps(self) -> pd.DataFrame:
        # Begin Program Section Record
        return self.get_record(StdfRecordType.bps)

    @property
    def pmr(self) -> pd.DataFrame:
        # Pin Map Record
        return self.get_record(StdfRecordType.pmr)

    @property
    def rdr(self) -> pd.DataFrame:
        # Retest Data Record
        return self.get_record(StdfRecordType.rdr)

    @property
    def ptr(self) -> pd.DataFrame:
        # Parametric Test Record
        return self.get_record(StdfRecordType.ptr)

    @property
    def eps(self) -> pd.DataFrame:
        # End Program Section Record
        return self.get_record(StdfRecordType.eps)

    @property
    def pcr(self) -> pd.DataFrame:
        # Part Count Record
        return self.get_record(StdfRecordType.pcr)

    @property
    def hbr(self) -> pd.DataFrame:
        # Hardware Bin Record
        return self.get_record(StdfRecordType.hbr)

    @property
    def wir(self) -> pd.DataFrame:
        # Wafer Information Record
        return self.get_record(StdfRecordType.wir)

    @property
    def sbr(self) -> pd.DataFrame:
        # Software Bin Record
        return self.get_record(StdfRecordType.sbr)

    @property
    def atr(self) -> pd.DataFrame:
        # Audit Trail Record
        return self.get_record(StdfRecordType.atr)

    @property
    def tsr(self) -> pd.DataFrame:
        # Test Synopsis Record
        return self.get_record(StdfRecordType.tsr)

    @property
    def far(self) -> pd.DataFrame:
        # File Attributes Record
        return self.get_record(StdfRecordType.far)

    @property
    def wrr(self) -> pd.DataFrame:
        # Wafer Results Record
        return self.get_record(StdfRecordType.wrr)

    @property
    def ftr(self) -> pd.DataFrame:
        # Functional Test Record
        return self.get_record(StdfRecordType.ftr)

    @property
    def prr(self) -> pd.DataFrame:
        # Part Results Record
        return self.get_record(StdfRecordType.prr)

    @property
    def plr(self) -> pd.DataFrame:
        # Pin List Record
        return self.get_record(StdfRecordType.plr)

    @property
    def dtr(self) -> pd.DataFrame:
        # Datalog Text Record
        return self.get_record(StdfRecordType.dtr)

    @property
    def wcr(self) -> pd.DataFrame:
        # Wafer Configuration Record
        return self.get_record(StdfRecordType.wcr)

    @property
    def mir(self) -> pd.DataFrame:
        # Master Information Record
        return self.get_record(StdfRecordType.mir)

    @property
    def mpr(self) -> pd.DataFrame:
        # Master Information Record
        return self.get_record(StdfRecordType.mpr)
