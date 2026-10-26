import sys, json
from pyspark import SparkContext

sc = SparkContext(appName="temperaturas_mapreduce")
sc.setLogLevel("WARN")

# ---------- MAP ----------
# Cada fichero entero es un array JSON: wholeTextFiles da (ruta, contenido)
# y flatMap emite un par (clave, valor) por registro.
def mapper(fichero):
    _, contenido = fichero
    for r in json.loads(contenido):
        tmax, tmin = float(r["TMAX"]), float(r["TMIN"])
        yield (r["NAME"], (tmax, r["DATE"], tmin, r["DATE"]))

# ---------- REDUCE ----------
# Combina dos valores de la misma clave: se queda con el TMAX mayor y el TMIN menor.
def reducer(a, b):
    mx = a[:2] if a[0] >= b[0] else b[:2]
    mn = a[2:] if a[2] <= b[2] else b[2:]
    return mx + mn

# 2 particiones = 2 reducers, como en Hadoop
por_estacion = (sc.wholeTextFiles(sys.argv[1])
                  .flatMap(mapper)
                  .reduceByKey(reducer, numPartitions=2))

# Resultados parciales de cada "reducer" (equivalente a part-00000 y part-00001)
for i, parte in enumerate(por_estacion.glom().collect()):
    print("--- part-0000%d ---" % i)
    for name, (tmax, dmax, tmin, dmin) in sorted(parte):
        print("%s\t%s\t%s\t%s\t%s" % (name, tmax, dmax, tmin, dmin))

# ---------- PASO FINAL (equivalente a combinar.py) ----------
calor = por_estacion.reduce(lambda a, b: a if a[1][0] >= b[1][0] else b)
frio  = por_estacion.reduce(lambda a, b: a if a[1][2] <= b[1][2] else b)
print("Más calor: %s -> %s °C (%s)" % (calor[0], calor[1][0], calor[1][1]))
print("Más frío:  %s -> %s °C (%s)" % (frio[0], frio[1][2], frio[1][3]))

sc.stop()