#!/usr/bin/env python3
# Cũng dùng làm Combiner được: phép cộng có tính kết hợp, đầu ra cùng định dạng key<TAB>value
import sys
from decimal import Decimal
from common import setup_io, fmt
setup_io()
cur, total = None, Decimal(0)
for line in sys.stdin:
    key, val = line.rstrip("\n").split("\t")
    if key != cur:
        if cur is not None:
            print(f"{cur}\t{fmt(total)}")
        cur, total = key, Decimal(0)
    total += Decimal(val)
if cur is not None:
    print(f"{cur}\t{fmt(total)}")
