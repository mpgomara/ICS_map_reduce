#!/usr/bin/env python3

import re, sys

pair = re.compile(r'"(\w+)"\s*:\s*"(.*?)"')
rec = {}

def num(s):
    return float(s)

for line in sys.stdin:
    m = pair.search(line)
    if m:
        rec[m.group(1)] = m.group(2)
    if "}" in line:                         # fin de registro
        if rec:
            tmax, tmin = num(rec.get("TMAX")), num(rec.get("TMIN"))
            name = rec.get("NAME", rec.get("STATION", "?"))
            if tmax is not None or tmin is not None:
                print('{0}\t{1}\t{2}\t{3}'.format(
                    name,
                    "" if tmax is None else tmax,
                    "" if tmin is None else tmin,
                    rec.get("DATE", "")))
        rec = {}