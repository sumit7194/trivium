#!/bin/zsh
# V20 driver: Kerr (2 partners) and TS at the capture-edge level, 4 variants each (rtol x s0). Guards: disk >= 5 GB.
cd "$(dirname "$0")"; PY=/Users/sumit/Github/conjecture_machine/.venv/bin/python
for rt in 1e-12 1e-13; do for s0 in ${=S0S:-1e-7 1e-8}; do
  for spec in "kerr45 97/100 2.55380 2.0 30.0 4.994777" "kerr45 97/100 2.550268 2.0 30.0 4.993305" "ts45 97/100 41/8 2.0 30.0 9.98"; do
    avail=$(df -g / | awk 'NR==2{print $4}'); [ "$avail" -lt 5 ] && { echo "DISK GUARD $avail GB"; exit 3; }
    set -- ${=spec}; tag="$1_L$3_r${rt}_s${s0}"; tag=${tag//\//_}
    nice -n 10 $PY v20.py $1 $2 $3 $rt $s0 $4 $5 $6 > ../results/$tag.json 2> ../results/$tag.err
    echo "$(date +%T) done $tag"
  done
done; done
