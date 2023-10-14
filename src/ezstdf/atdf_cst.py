from .stdf_cst import StdfRecordType, stdf_record_fields


atdf_record_fields = {
    StdfRecordType.far: ('CPU_TYPE', 'STDF_VER', 'ATDF Version', 'Scaling Flag'),
    StdfRecordType.atr: ('MOD_TIM', 'CMD_LINE'),
    StdfRecordType.mir: (
        'LOT_ID', 'PART_TYP', 'JOB_NAM', 'NODE_NAM', 'TSTR_TYP', 'SETUP_T', 'START_T', 'OPER_NAM',
        'MODE_COD', 'STAT_NUM', 'SBLOT_ID', 'TEST_COD', 'RTST_COD', 'JOB_REV', 'EXEC_TYP', 'EXEC_VER',
        'PROT_COD', 'CMOD_COD', 'BURN_TIM', 'TST_TEMP', 'USER_TXT', 'AUX_FILE', 'PKG_TYP', 'FAMLY_ID',
        'DATE_COD', 'FACIL_ID', 'FLOOR_ID', 'PROC_ID', 'OPER_FRQ', 'SPEC_NAM', 'SPEC_VER', 'FLOW_ID',
        'SETUP_ID', 'DSGN_REV', 'ENG_ID', 'ROM_COD', 'SERL_NUM', 'SUPR_NAM'
        ),
    StdfRecordType.mrr: stdf_record_fields[StdfRecordType.mrr],
    StdfRecordType.pcr: stdf_record_fields[StdfRecordType.pcr],
    StdfRecordType.hbr: stdf_record_fields[StdfRecordType.hbr],
    StdfRecordType.sbr: stdf_record_fields[StdfRecordType.sbr],
    StdfRecordType.pmr: stdf_record_fields[StdfRecordType.pmr],
    StdfRecordType.pgr: ('GRP_INDX', 'GRP_NAM', 'PMR_INDX'),
    StdfRecordType.plr: ('GRP_INDX', 'GRP_MODE', 'GRP_RADX', 'PGM_CHAR', 'RTN_CHAR'),
    StdfRecordType.rdr: ('RTST_BIN',),
    StdfRecordType.sdr: (
        'HEAD_NUM', 'SITE_GRP', 'SITE_NUM', 'HAND_TYP', 'HAND_ID', 'CARD_TYP', 'CARD_ID', 'LOAD_TYP',
        'LOAD_ID',
        'DIB_TYP', 'DIB_ID', 'CABL_TYP', 'CABL_ID', 'CONT_TYP', 'CONT_ID', 'LASR_TYP', 'LASR_ID', 'EXTR_TYP',
        'EXTR_ID'),
    StdfRecordType.wir: ('HEAD_NUM', 'START_T', 'SITE_GRP', 'WAFER_ID'),
    StdfRecordType.wrr: (
        'HEAD_NUM', 'FINISH_T', 'PART_CNT', 'WAFER_ID', 'SITE_GRP', 'RTST_CNT', 'ABRT_CNT', 'GOOD_CNT',
        'FUNC_CNT', 'FABWF_ID', 'FRAME_ID', 'MASK_ID', 'USR_DESC', 'EXC_DESC'
    ),
    StdfRecordType.wcr: (
        'WF_FLAT', 'POS_X', 'POS_Y', 'WAFR_SIZ', 'DIE_HT', 'DIE_WID', 'WF_UNITS', 'CENTER_X', 'CENTER_Y'),
    StdfRecordType.pir: stdf_record_fields[StdfRecordType.pir],
    StdfRecordType.prr: (
        'HEAD_NUM', 'SITE_NUM', 'PART_ID', 'NUM_TEST', 'PART_FLG_3_4', 'HARD_BIN', 'SOFT_BIN', 'X_COORD', 'Y_COORD',
        'PART_FLG_0_1', 'PART_FLG_2', 'TEST_T', 'PART_TXT', 'PART_FIX'
    ),
    StdfRecordType.tsr: (
        'HEAD_NUM', 'SITE_NUM', 'TEST_NUM', 'TEST_NAM', 'TEST_TYP', 'EXEC_CNT', 'FAIL_CNT', 'ALRM_CNT',
        'SEQ_NAME', 'TEST_LBL', 'TEST_TIM', 'TEST_MIN', 'TEST_MAX', 'TST_SUMS', 'TST_SQRS'
    ),
    StdfRecordType.ptr: (
        'TEST_NUM', 'HEAD_NUM', 'SITE_NUM', 'RESULT', 'TEST_FLG_6_7', 'TEST_FLG_0_2_3_4_5', "TEST_TXT",
        'ALARM_ID', 'PARM_FLG_6_7', 'UNITS', 'LO_LIMIT', 'HI_LIMIT', 'C_RESFMT', 'C_LLMFMT', 'C_HLMFMT',
        'LO_SPEC', 'HI_SPEC', 'RES_SCAL', 'LLM_SCAL', 'HLM_SCAL'
    ),
    StdfRecordType.mpr: (
        'TEST_NUM', 'HEAD_NUM', 'SITE_NUM', 'RTN_STAT', 'RTN_RSLT', 'TEST_FLG_6_7', 'TEST_FLG_0_2_3_4_5', 'TEST_TXT',
        'ALARM_ID', 'PARM_FLG_6_7', 'UNITS', 'LO_LIMIT', 'HI_LIMIT', 'START_IN', 'INCR_IN', 'UNITS_IN', 'RTN_INDX',
        'C_RESFMT', 'C_LLMFMT', 'C_HLMFMT', 'LO_SPEC', 'HI_SPEC', 'RES_SCAL', 'LLM_SCAL', 'HLM_SCAL'
    ),
    StdfRecordType.ftr: (
        'TEST_NUM', 'HEAD_NUM', 'SITE_NUM', 'TEST_FLG_6_7', 'TEST_FLAG_0_2_3_4_5', 'VECT_NAM', 'TIME_SET', 'CYCL_CNT',
        'REL_VADR', 'REPT_CNT', 'NUM_FAIL', 'XFAIL_AD', 'YFAIL_AD', 'VECT_OFF', 'RTN_INDX', 'RTN_STAT', 'PGM_INDX',
        'PGM_STAT', 'FAIL_PIN', 'OP_CODE', 'TEST_TXT', 'ALARM_ID', 'PROG_TXT', 'RSLT_TXT', 'PATG_NUM', 'SPIN_MAP'
    ),
    StdfRecordType.bps: stdf_record_fields[StdfRecordType.bps],
    StdfRecordType.eps: stdf_record_fields[StdfRecordType.eps],
    StdfRecordType.gdr: ('GEN_DATA',),
    StdfRecordType.dtr: stdf_record_fields[StdfRecordType.dtr],
}
