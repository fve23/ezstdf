from ezstdf.StdfReader import StdfReader
import time


stdf = StdfReader()

t_start = time.perf_counter()
stdf.parse_file("../sample_files/ROOS_20140728_131230.stdf")
# stdf.parse_file("../sample_files/sample.atdf")
t_stop = time.perf_counter()

print("Parsed", stdf.get_total_record_count(), "records in", t_stop - t_start)

print(stdf.far)
# stdf.to_excel("test.xlsx")
