#!/bin/bash
IN=${1:-input_ext.txt}
OUT=${2:-out}
PY=${PY:-python}
mkdir -p "$OUT"
export PYTHONIOENCODING=utf-8
TAB=$'\t'
srt() { LC_ALL=C sort -t "$TAB" -k1,1; }

# ===== JOB 1: chuẩn hóa + khử trùng theo mã đơn =====
$PY clean_mapper.py < "$IN" 2> "$OUT/audit_job1_map.txt" \
  | tee "$OUT/1_map_job1.txt" | srt | tee "$OUT/2_shuffle_job1.txt" \
  | $PY dedup_reducer.py 2> "$OUT/audit_job1_reduce.txt" > "$OUT/3_reduce_job1.txt"

# ===== JOB 2: lọc nghiệp vụ + tổng hợp nhiều khóa =====
$PY sum_mapper.py < "$OUT/3_reduce_job1.txt" 2> "$OUT/audit_job2_map.txt" \
  | tee "$OUT/4_map_job2.txt" | srt | tee "$OUT/5_shuffle_job2.txt" \
  | $PY sum_reducer.py > "$OUT/result.txt"

cat "$OUT"/audit_*.txt > "$OUT/audit_all.txt"
echo "Dong vao        : $(wc -l < "$IN")"
echo "Don duy nhat    : $(wc -l < "$OUT/3_reduce_job1.txt")"
echo "Cap Map (job 2) : $(wc -l < "$OUT/4_map_job2.txt")"
echo "Dong audit      : $(wc -l < "$OUT/audit_all.txt")"
echo "Ket qua         : $OUT/result.txt"
