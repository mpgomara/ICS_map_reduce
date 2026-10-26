#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


DIRECTORY = Path(__file__).resolve().parent
STATIONS_FILE = DIRECTORY / "estaciones.txt"
BASE_URL = "https://www.ncei.noaa.gov/access/services/data/v1"


def main(output_directory=DIRECTORY):
    failures = []

    with STATIONS_FILE.open(encoding="utf-8") as stations_file:
        station_ids = []
        for line_number, line in enumerate(stations_file, start=1):
            if not line.strip():
                continue
            station_id = line.split()[0].rstrip(",")
            if not station_id:
                raise ValueError(f"ID de estación vacío en la línea {line_number}")
            station_ids.append(station_id)

    output_directory.mkdir(parents=True, exist_ok=True)

    for station_id in station_ids:
        parameters = {
            "dataset": "daily-summaries",
            "stations": station_id,
            "startDate": "2025-01-01",
            "endDate": "2025-12-31",
            "dataTypes": "TMAX,TMIN",
            "format": "json",
            "units": "metric",
            "includeStationName": "true",
            "includeStationLocation": "false",
        }
        url = f"{BASE_URL}?{urlencode(parameters)}"
        output_file = output_directory / f"{station_id}_daily-summaries_2025.json"

        try:
            with urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
            with output_file.open("w", encoding="utf-8") as result_file:
                json.dump(data, result_file, ensure_ascii=False, indent=2)
                result_file.write("\n")
            print(f"Guardado: {output_file}")
        except (HTTPError, URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError, OSError) as error:
            print(f"Error consultando {station_id}: {error}", file=sys.stderr)
            failures.append(station_id)

    if failures:
        print(f"Fallaron las consultas para: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descarga resúmenes diarios de estaciones NOAA.")
    parser.add_argument(
        "output_directory",
        nargs="?",
        type=Path,
        default=DIRECTORY,
        help="Carpeta para guardar los JSON (por defecto: la carpeta del script).",
    )
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.output_directory))