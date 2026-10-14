#!/usr/bin/env python3
import random, sys, unicodedata
from collections import deque
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
random.seed(42)

NV = ["An", "Bình", "Chi", "Dũng", "Lan", "Minh", "Nam", "Hà"]
W = [50, 10, 10, 8, 8, 6, 4, 4]                  # An chiếm 50% -> data skew
CN_OLD = ["Hà Nội", "Đà Nẵng", "TP.HCM"]
CN_NEW = ["Hải Phòng", "Cần Thơ"]

def no_accent(s):
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def v_nv(n):
    r = random.random()
    if r < 0.80: return n
    if r < 0.86: return n.upper()
    if r < 0.90: return "  " + n.lower() + " "
    if r < 0.95: return no_accent(n)
    return (n + n[-1]) if len(no_accent(n)) >= 3 else n.upper()

def v_cn(c):
    r = random.random()
    if r < 0.85: return c
    if r < 0.92: return c.upper()
    if c in CN_OLD and r < 0.97: return no_accent(c)
    return " " + c.lower() + " "

truth = {}
def add(k, v): truth[k] = truth.get(k, 0) + v

hist = deque(maxlen=1000)
with open("big_input.txt", "w", encoding="utf-8", newline="\n") as f:
    for i in range(N):
        r = random.random()
        if r < 0.02 and hist:                                   # đơn trùng mã
            ma, cn, nv, gt, tt = random.choice(hist)
            f.write(f"{ma},{v_cn(cn)},{v_nv(nv)},{gt},{tt}\n"); continue
        if r < 0.025:                                           # thiếu trường
            f.write(f"{100000+i},{random.choice(CN_OLD)},{random.choice(NV)},{random.randint(10,500)}\n"); continue
        if r < 0.03:                                            # giá trị không phải số
            f.write(f"{100000+i},{random.choice(CN_OLD)},{random.choice(NV)},N/A,THANH_CONG\n"); continue
        ma = 100000 + i
        cn = random.choice(CN_OLD + CN_NEW)
        nv = random.choices(NV, W)[0]
        x = random.random()
        if x < 0.08:   tt, gt = "HOAN_TRA", random.randint(10, 500)
        elif x < 0.09: tt, gt = "THANH_CONG", -random.randint(1, 50)
        else:          tt, gt = "THANH_CONG", random.randint(10, 500)
        hist.append((ma, cn, nv, gt, tt))
        f.write(f"{ma},{v_cn(cn)},{v_nv(nv)},{gt},{tt}\n")
        if tt == "THANH_CONG" and gt >= 0:
            add(f"NV|{nv}", gt); add(f"CN|{cn}", gt); add(f"CNNV|{cn}|{nv}", gt); add("TONG|ALL", gt)

with open("expected.txt", "w", encoding="utf-8", newline="\n") as f:
    for k in sorted(truth): f.write(f"{k}\t{truth[k]}\n")
print("Da tao big_input.txt va expected.txt")
