#!/usr/bin/env python3
import sys

cur, total = None, 0.0
for line in sys.stdin:
    key, val = line.rstrip("\n").split("\t")
    if key != cur:
        if cur is not None:
            print(f"{cur}\t{total:g}")
        cur, total = key, 0.0
    total += float(val)
if cur is not None:
    print(f"{cur}\t{total:g}")