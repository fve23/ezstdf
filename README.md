# ezstdf

ezstdf is a python package for parsing "Standard Test Data Format" files with a focus on speed.
Parse a STDF file with thousands of records in less than a second.

## Installation
```
pip install --upgrade ezstdf
```

### Dependencies
- pandas (required)


## Features
- Can read STDF (binary, V4) and ATDF (clear text, V2) files
- Most record types are supported, unsupported ones are skipped for now
- Convert records to Pandas data frames
- Export to Excel file (requires openpyxl)
- Auto-detection of endianness
- Fast and easy to use


## Examples
Parse a file:
```python
from ezstdf.StdfReader import StdfReader
stdf = StdfReader()
stdf.parse_file("../sample_files/sample.atdf")

# each record type can now be accessed as a data frame
# example: access the File Attributes Record (FAR)
df_far = stdf.far
print(df_far)
```

Export as Excel. Each sheet is a difference record, and each row a sub-record.
```python
stdf.to_excel("test.xlsx")
```

## History
- v0.0.1: initial release
- v0.0.2: fixed meta info in pypi
- v0.0.3:
  - better tolerance to illegal characters in strings
  - fixed parsing of jx and kx fields
  - support for mpr