#!/usr/bin/env python3
import sys
from common import setup_io, audit
setup_io()

def flush(ma, recs):
    if ma is None:
        return
    uniq = sorted(set(recs))
    if len(recs) > 1:
        audit("TRUNG_MA", ma, f"{len(recs)} ban ghi")
    if len(uniq) > 1:                       # cùng mã nhưng nội dung khác nhau
        audit("XUNG_DOT", ma, " || ".join(uniq))
        return                              # không đoán: loại hẳn, chuyển đối soát
    print(f"{ma}\t{uniq[0]}")

cur, recs = None, []
for line in sys.stdin:
    ma, rec = line.rstrip("\n").split("\t", 1)
    if ma != cur:
        flush(cur, recs)
        cur, recs = ma, []
    recs.append(rec)
flush(cur, recs)
