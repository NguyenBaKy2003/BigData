#!/usr/bin/env python3
import sys
from decimal import Decimal
from common import setup_io, fmt, audit
setup_io()
for line in sys.stdin:
    ma, rec = line.rstrip("\n").split("\t", 1)
    cn, nv, gt, tt = rec.split("|")
    d = Decimal(gt)
    if tt != "THANH_CONG":
        audit("LOAI_TRANG_THAI", ma, f"{tt} {gt}"); continue
    if d < 0:
        audit("LOAI_TIEN_AM", ma, f"{tt} {gt}"); continue
    v = fmt(d)
    print(f"NV|{nv}\t{v}")
    print(f"CN|{cn}\t{v}")
    print(f"CNNV|{cn}|{nv}\t{v}")
    print(f"TONG|ALL\t{v}")
