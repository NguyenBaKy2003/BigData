#!/usr/bin/env python3
import sys
from decimal import Decimal, InvalidOperation
from common import setup_io, canon_nv, canon_cn, fmt, audit
setup_io()
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    p = [x.strip() for x in line.split(",")]
    if len(p) != 5:
        audit("THIEU_TRUONG", "?", line); continue
    ma, cn, nv, gt, tt = p
    if not ma:
        audit("THIEU_MA", "?", line); continue
    try:
        d = Decimal(gt)
        if not d.is_finite():
            raise InvalidOperation
    except InvalidOperation:
        audit("GIA_TRI_LOI", ma, gt); continue
    nv2, flag = canon_nv(nv)
    if nv2 is None:
        audit("NV_TRONG", ma, line); continue
    if flag:
        audit(flag, ma, f"{nv!r} -> {nv2}")
    cn2 = canon_cn(cn)
    if cn2 is None:
        audit("CN_TRONG", ma, line); continue
    print(f"{ma}\t{cn2}|{nv2}|{fmt(d)}|{tt.upper()}")
