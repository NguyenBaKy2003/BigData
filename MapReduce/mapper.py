#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) != 5:
        print(f"ERROR\t{line.strip()}|thieu_truong", file=sys.stderr)
        continue
    ma, cn, nv, gt, tt = parts
    try:
        gt = float(gt)
    except ValueError:
        print(f"ERROR\t{ma}|gia_tri_khong_phai_so", file=sys.stderr)
        continue
    if tt == "THANH_CONG" and gt >= 0:
        print(f"{nv}\t{gt}")
    else:
        print(f"REJECT\t{ma}|{tt}|{gt}", file=sys.stderr)  # để đối soát