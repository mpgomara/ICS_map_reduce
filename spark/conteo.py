import sys
from pyspark.sql import SparkSession


def mapper(linea):
    for palabra in linea.lower().split():
        yield (palabra, 1)


def reducer(grupo):
    palabra, valores = grupo
    total = 0
    for valor in valores:
        total += valor
    return (palabra, total)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: spark-submit conteo.py entrada salida")

    spark = SparkSession.builder.appName("ConteoLibros").getOrCreate()
    sc = spark.sparkContext

    try:
        lineas = sc.textFile(sys.argv[1])

        # MAP
        pares = lineas.flatMap(mapper)

        # SHUFFLE: agrupar por palabra en cuatro particiones
        grupos = pares.groupByKey(numPartitions=4)

        # REDUCE
        resultado = grupos.map(reducer)

        # Ejecutar el trabajo y guardar todos los resultados
        resultado.saveAsTextFile(sys.argv[2])
        #grupos.saveAsTextFile('intermedio')
    finally:
        spark.stop()