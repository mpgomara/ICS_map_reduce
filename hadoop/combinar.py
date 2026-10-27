#!/usr/bin/env python3
import sys

rows = []
for line in sys.stdin:
    name, tmax, dmax, tmin, dmin = line.rstrip("\n").split("\t")
    rows.append((name, float(tmax) if tmax != "None" else None, dmax,
                 float(tmin) if tmin != "None" else None, dmin))

hot = max((r for r in rows if r[1] is not None), key=lambda r: r[1])
cold = min((r for r in rows if r[3] is not None), key=lambda r: r[3])
print("Más calor: %s -> %s °C (%s)" % (hot[0], hot[1], hot[2]))
print("Más frío:  %s -> %s °C (%s)" % (cold[0], cold[3], cold[4]))