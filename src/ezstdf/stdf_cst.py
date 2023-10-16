from enum import Enum
from .parsers import *


"""
Constants based on:
    Standard Test Data Format
    (STDF)
    Specification
    Version 4
"""


class StdfRecordType(Enum):
    # 0 "Information about the STDF file"
    far = (0, 10)  # "File Attributes Record (FAR)"
    atr = (0, 20)  # "Audit Trail Record (ATR)"
    # 1 "Data collected on a per lot basis"
    mir = (1, 10)  # "Master Information Record (MIR)"
    mrr = (1, 20)  # "Master Results Record (MRR)"
    pcr = (1, 30)  # "Part Count Record (PCR)"
    hbr = (1, 40)  # "Hardware Bin Record (HBR)"
    sbr = (1, 50)  # "Software Bin Record (SBR)"
    pmr = (1, 60)  # "Pin Map Record (PMR)"
    pgr = (1, 62)  # "Pin Group Record (PGR)"
    plr = (1, 63)  # "Pin List Record (PLR)"
    rdr = (1, 70)  # "Retest Data Record (RDR)"
    sdr = (1, 80)  # "Site Description Record (SDR)"
    # 2 "Data collected per wafer"
    wir = (2, 10)  # "Wafer Information Record (WIR)"
    wrr = (2, 20)  # "Wafer Results Record (WRR)"
    wcr = (2, 30)  # "Wafer Configuration Record (WCR)"
    # 5 "Data collected on a per part basis"
    pir = (5, 10)  # "Part Information Record (PIR)"
    prr = (5, 20)  # "Part Results Record (PRR)"
    # 10 "Data collected per test in the test program"
    tsr = (10, 30)  # "Test Synopsis Record (TSR)"
    # 15 "Data collected per test execution"
    ptr = (15, 10)  # "Parametric Test Record (PTR)"
    mpr = (15, 15)  # "Multiple-Result Parametric Record (MPR)"
    ftr = (15, 20)  # "Functional Test Record (FTR)"
    # 20 "Data collected per program segment"
    bps = (20, 10)  # "Begin Program Section Record (BPS)"
    eps = (20, 20)  # "End Program Section Record (EPS)"
    # 50 "Generic Data"
    gdr = (50, 10)  # "Generic Data Record (GDR)"
    dtr = (50, 30)  # "Datalog Text Record (DTR)"


stdf_record_parsers = {
    StdfRecordType.mpr: (
        parse_u32, parse_u8, parse_u8, parse_u8, parse_u8,
        parse_u16, parse_u16, parse_nibble_array_jx, parse_float_array_kx,
        parse_str, parse_str,
        parse_byte, parse_i8, parse_i8, parse_i8, parse_float, parse_float, parse_float, parse_float,
        parse_u16_array_jx, parse_str, parse_str, parse_str, parse_str, parse_str, parse_float, parse_float
    ),
    StdfRecordType.far: (parse_u8, parse_u8),
    StdfRecordType.atr: (parse_date, parse_str),
    StdfRecordType.mir: (
        parse_date, parse_date, parse_u8, parse_u8, parse_u8, parse_u8, parse_u16, parse_u8, parse_str, parse_str,
        parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str,
        parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str,
        parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str),
    StdfRecordType.mrr: (parse_date, parse_u8, parse_str, parse_str),
    StdfRecordType.pcr: (parse_u8, parse_u8, parse_u32, parse_u32, parse_u32, parse_u32, parse_u32),
    StdfRecordType.hbr: (parse_u8, parse_u8, parse_u16, parse_u32, parse_u8, parse_str),
    StdfRecordType.sbr: (parse_u8, parse_u8, parse_u16, parse_u32, parse_u8, parse_str),
    StdfRecordType.pmr: (parse_u16, parse_u16, parse_str, parse_str, parse_str, parse_u8, parse_u8),
    StdfRecordType.pgr: (parse_u16, parse_str, parse_u16, parse_u16_array_kx),
    StdfRecordType.plr: (
        parse_u16, parse_u16_array_kx, parse_u16_array_kx, parse_u8_array_kx,
        parse_str_array_kx, parse_str_array_kx, parse_str_array_kx, parse_str_array_kx),
    StdfRecordType.rdr: (parse_u16, parse_u16_array_kx),
    StdfRecordType.sdr: (
        parse_u8, parse_u8, parse_u8, parse_u8_array_kx, parse_str, parse_str, parse_str,
        parse_str, parse_str, parse_str,
        parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str, parse_str),
    StdfRecordType.wir: (parse_u8, parse_u8, parse_date, parse_str),
    StdfRecordType.wrr: (
        parse_u8, parse_u8, parse_date, parse_u32, parse_u32, parse_u32, parse_u32, parse_u32, parse_str, parse_str,
        parse_str, parse_str, parse_str, parse_str),
    StdfRecordType.wcr: (
        parse_float, parse_float, parse_float, parse_u8, parse_u8, parse_i16, parse_i16, parse_u8, parse_u8),
    StdfRecordType.pir: (parse_u8, parse_u8),
    StdfRecordType.prr: (
        parse_u8, parse_u8, parse_u8, parse_u16, parse_u16, parse_u16, parse_i16, parse_i16, parse_u32, parse_str,
        parse_str, parse_u8_array),
    StdfRecordType.tsr: (
        parse_u8, parse_u8, parse_u8, parse_u32, parse_u32, parse_u32, parse_u32, parse_str, parse_str, parse_str,
        parse_u8,
        parse_float, parse_float, parse_float, parse_float, parse_float),
    StdfRecordType.ptr: (
        parse_u32, parse_u8, parse_u8, parse_u8, parse_u8, parse_float, parse_str, parse_str, parse_u8, parse_i8,
        parse_i8,
        parse_i8, parse_float, parse_float, parse_str, parse_str, parse_str, parse_str, parse_float, parse_float),
    StdfRecordType.ftr: (
        parse_u32, parse_u8, parse_u8, parse_u8, parse_u8, parse_u32, parse_u32, parse_u32, parse_u32, parse_i32,
        parse_i32,
        parse_i16, parse_u16, parse_u16, parse_u16_array_jx, parse_u8_array_jx,
        parse_u16_array_kx, parse_u8_array_kx, parse_str, parse_bit_fields, parse_str, parse_str,
        parse_str, parse_str, parse_str, parse_str, parse_u8, parse_bit_fields),
    StdfRecordType.bps: (parse_str,),
    StdfRecordType.eps: (),
    StdfRecordType.gdr: (parse_u16, parse_variable_field),
    StdfRecordType.dtr: (parse_str,),
}


stdf_record_fields = {
    StdfRecordType.mpr: (
        'TEST_NUM', 'HEAD_NUM', 'SITE_NUM', 'TEST_FLG', 'PARM_FLG', 'RTN_ICNT', 'RSLT_CNT', 'RTN_STAT', 'RTN_RSLT',
        'TEST_TXT', 'ALARM_ID', 'OPT_FLAG', 'RES_SCAL', 'LLM_SCAL', 'HLM_SCAL', 'LO_LIMIT', 'HI_LIMIT', 'START_IN',
        'INCR_IN', 'RTN_INDX', 'UNITS', 'UNITS_IN', 'C_RESFMT', 'C_LLMFMT', 'C_HLMFMT', 'LO_SPEC', 'HI_SPEC'
        ),
    StdfRecordType.far: ('CPU_TYPE', 'STDF_VER'),
    StdfRecordType.atr: ('MOD_TIM', 'CMD_LINE'),
    StdfRecordType.mir: (
        'SETUP_T', 'START_T', 'STAT_NUM', 'MODE_COD', 'RTST_COD', 'PROT_COD', 'BURN_TIM', 'CMOD_COD', 'LOT_ID',
        'PART_TYP',
        'NODE_NAM', 'TSTR_TYP', 'JOB_NAM', 'JOB_REV', 'SBLOT_ID', 'OPER_NAM', 'EXEC_TYP', 'EXEC_VER', 'TEST_COD',
        'TST_TEMP', 'USER_TXT', 'AUX_FILE', 'PKG_TYP', 'FAMLY_ID', 'DATE_COD', 'FACIL_ID', 'FLOOR_ID', 'PROC_ID',
        'OPER_FRQ', 'SPEC_NAM', 'SPEC_VER', 'FLOW_ID', 'SETUP_ID', 'DSGN_REV', 'ENG_ID', 'ROM_COD', 'SERL_NUM',
        'SUPR_NAM'),
    StdfRecordType.mrr: ('FINISH_T', 'DISP_COD', 'USR_DESC', 'EXC_DESC'),
    StdfRecordType.pcr: ('HEAD_NUM', 'SITE_NUM', 'PART_CNT', 'RTST_CNT', 'ABRT_CNT', 'GOOD_CNT', 'FUNC_CNT'),
    StdfRecordType.hbr: ('HEAD_NUM', 'SITE_NUM', 'HBIN_NUM', 'HBIN_CNT', 'HBIN_PF', 'HBIN_NAM'),
    StdfRecordType.sbr: ('HEAD_NUM', 'SITE_NUM', 'SBIN_NUM', 'SBIN_CNT', 'SBIN_PF', 'SBIN_NAM'),
    StdfRecordType.pmr: ('PMR_INDX', 'CHAN_TYP', 'CHAN_NAM', 'PHY_NAM', 'LOG_NAM', 'HEAD_NUM', 'SITE_NUM'),
    StdfRecordType.pgr: ('GRP_INDX', 'GRP_NAM', 'INDX_CNT', 'PMR_INDX'),
    StdfRecordType.plr: ('GRP_CNT', 'GRP_INDX', 'GRP_MODE', 'GRP_RADX', 'PGM_CHAR', 'RTN_CHAR', 'PGM_CHAL', 'RTN_CHAL'),
    StdfRecordType.rdr: ('NUM_BINS', 'RTST_BIN'),
    StdfRecordType.sdr: (
        'HEAD_NUM', 'SITE_GRP', 'SITE_CNT', 'SITE_NUM', 'HAND_TYP', 'HAND_ID', 'CARD_TYP', 'CARD_ID', 'LOAD_TYP',
        'LOAD_ID',
        'DIB_TYP', 'DIB_ID', 'CABL_TYP', 'CABL_ID', 'CONT_TYP', 'CONT_ID', 'LASR_TYP', 'LASR_ID', 'EXTR_TYP',
        'EXTR_ID'),
    StdfRecordType.wir: ('HEAD_NUM', 'SITE_GRP', 'START_T', 'WAFER_ID'),
    StdfRecordType.wrr: (
        'HEAD_NUM', 'SITE_GRP', 'FINISH_T', 'PART_CNT', 'RTST_CNT', 'ABRT_CNT', 'GOOD_CNT', 'FUNC_CNT', 'WAFER_ID',
        'FABWF_ID', 'FRAME_ID', 'MASK_ID', 'USR_DESC', 'EXC_DESC'),
    StdfRecordType.wcr: (
        'WAFR_SIZ', 'DIE_HT', 'DIE_WID', 'WF_UNITS', 'WF_FLAT', 'CENTER_X', 'CENTER_Y', 'POS_X', 'POS_Y'),
    StdfRecordType.pir: ('HEAD_NUM', 'SITE_NUM'),
    StdfRecordType.prr: (
        'HEAD_NUM', 'SITE_NUM', 'PART_FLG', 'NUM_TEST', 'HARD_BIN', 'SOFT_BIN', 'X_COORD', 'Y_COORD', 'TEST_T',
        'PART_ID',
        'PART_TXT', 'PART_FIX'),
    StdfRecordType.tsr: (
        'HEAD_NUM', 'SITE_NUM', 'TEST_TYP', 'TEST_NUM', 'EXEC_CNT', 'FAIL_CNT', 'ALRM_CNT', 'TEST_NAM', 'SEQ_NAME',
        'TEST_LBL', 'OPT_FLAG', 'TEST_TIM', 'TEST_MIN', 'TEST_MAX', 'TST_SUMS', 'TST_SQRS'),
    StdfRecordType.ptr: (
        'TEST_NUM', 'HEAD_NUM', 'SITE_NUM', 'TEST_FLG', 'PARM_FLG', 'RESULT', 'TEST_TXT', 'ALARM_ID', 'OPT_FLAG',
        'RES_SCAL', 'LLM_SCAL', 'HLM_SCAL', 'LO_LIMIT', 'HI_LIMIT', 'UNITS', 'C_RESFMT', 'C_LLMFMT', 'C_HLMFMT',
        'LO_SPEC',
        'HI_SPEC'),
    StdfRecordType.ftr: (
        'TEST_NUM', 'HEAD_NUM', 'SITE_NUM', 'TEST_FLG', 'OPT_FLAG', 'CYCL_CNT', 'REL_VADR', 'REPT_CNT', 'NUM_FAIL',
        'XFAIL_AD', 'YFAIL_AD', 'VECT_OFF', 'RTN_ICNT', 'PGM_ICNT', 'PGM_INDX', 'PGM_STAT', 'FAIL_PIN', 'VECT_NAM',
        'TIME_SET', 'OP_CODE', 'TEST_TXT', 'ALARM_ID', 'PROG_TXT', 'RSLT_TXT', 'PATG_NUM', 'SPIN_MAP'),
    StdfRecordType.bps: ('SEQ_NAME',),
    StdfRecordType.eps: (),
    StdfRecordType.gdr: ('FLD_CNT', 'GEN_DATA'),
    StdfRecordType.dtr: ('TEXT_DAT',),
}
