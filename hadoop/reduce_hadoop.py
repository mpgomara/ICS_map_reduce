#!/usr/bin/env python

import sys
from itertools import groupby

def parse(line):
    name, tmax, tmin, date = line.rstrip("\n").split("\t")
    return name, (float(tmax) if tmax else None), (float(tmin) if tmin else None), date

rows = (parse(l) for l in sys.stdin if l.strip())
for name, grp in groupby(rows, key=lambda r: r[0]):
    best_max = (None, "")
    best_min = (None, "")
    for _, tmax, tmin, date in grp:
        if tmax is not None and (best_max[0] is None or tmax > best_max[0]):
            best_max = (tmax, date)
        if tmin is not None and (best_min[0] is None or tmin < best_min[0]):
            best_min = (tmin, date)
    print("%s\t%s\t%s\t%s\t%s" % (name, best_max[0], best_max[1], best_min[0], best_min[1]))