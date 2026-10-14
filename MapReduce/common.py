import sys, re, unicodedata, difflib
from decimal import Decimal

KNOWN_NV = ["An", "Bình", "Chi", "Dũng", "Lan", "Minh", "Nam", "Hà"]
KNOWN_CN = ["Hà Nội", "Đà Nẵng", "TP.HCM"]   # chi nhánh khác = chi nhánh mới, vẫn được chấp nhận

def setup_io():
    for s in (sys.stdin, sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")

def fold(s):
    """bỏ dấu, hạ chữ thường, gộp khoảng trắng"""
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip().lower()

_NV = {fold(n): n for n in KNOWN_NV}
_CN = {fold(n): n for n in KNOWN_CN}

def tidy(s):
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", s)).strip().replace("|", " ")

def canon_nv(raw):
    k = fold(raw)
    if not k:
        return None, "NV_TRONG"
    if k in _NV:
        return _NV[k], None
    if len(k) >= 3:                              # chỉ sửa chính tả với tên >= 3 ký tự
        m = difflib.get_close_matches(k, list(_NV), n=1, cutoff=0.8)
        if m:
            return _NV[m[0]], "NV_SUA"
    return tidy(raw).title(), "NV_LA"

def canon_cn(raw):
    k = fold(raw)
    if not k:
        return None
    return _CN.get(k) or tidy(raw).title()

def fmt(d):
    s = format(d, "f")
    return s.rstrip("0").rstrip(".") if "." in s else s

def audit(kind, ma, detail):
    print(f"AUDIT\t{kind}\t{ma}\t{detail}", file=sys.stderr)
