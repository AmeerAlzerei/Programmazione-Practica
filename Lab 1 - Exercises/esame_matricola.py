import os


class ExamException(Exception):
    pass


class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        time_series = []
        previous_timestamp = None
        seen_timestamps = set()

        # Il controllo sul file viene fatto qui, come richiesto dalla traccia.
        try:
            file = open(self.name, "r")
        except OSError:
            raise ExamException("Errore, file non apribile")

        with file:
            for line in file:
                elements = line.strip().split(",")

                # Le righe incomplete o non leggibili vengono ignorate senza fermare il programma.
                if len(elements) < 2:
                    print("Riga ignorata: dati incompleti")
                    continue

                timestamp = elements[0]
                passengers = elements[1]

                # Un timestamp non valido viene ignorato, per esempio l'intestazione del CSV.
                if not self._is_valid_timestamp(timestamp):
                    print("Riga ignorata: timestamp non valido")
                    continue

                # Timestamp duplicati o fuori ordine sono invece errori bloccanti.
                if timestamp in seen_timestamps:
                    raise ExamException("Errore, timestamp duplicato")

                if previous_timestamp is not None and timestamp < previous_timestamp:
                    raise ExamException("Errore, timestamp fuori ordine")

                # Il numero di passeggeri deve essere intero e non negativo.
                try:
                    passengers = int(passengers)
                except ValueError:
                    print("Riga ignorata: valore passeggeri non intero")
                    continue

                if passengers < 0:
                    print("Riga ignorata: valore passeggeri negativo")
                    continue

                time_series.append([timestamp, passengers])
                seen_timestamps.add(timestamp)
                previous_timestamp = timestamp

        return time_series

    def _is_valid_timestamp(self, timestamp):
        elements = timestamp.split("-")

        if len(elements) != 2:
            return False

        year = elements[0]
        month = elements[1]

        if len(year) != 4 or len(month) != 2:
            return False

        if not year.isdigit() or not month.isdigit():
            return False

        month = int(month)
        return 1 <= month <= 12


def compute_variations(time_series, first_year, last_year):
    # Controllo degli input principali della funzione.
    if not isinstance(time_series, list):
        raise ExamException("Errore, la serie temporale deve essere una lista")

    if not _is_valid_year(first_year) or not _is_valid_year(last_year):
        raise ExamException("Errore, gli estremi dell'intervallo devono essere stringhe nel formato YYYY")

    if first_year > last_year:
        raise ExamException("Errore, il primo anno deve precedere o coincidere con l'ultimo")

    passengers_by_year = {}

    # Raggruppo i passeggeri per anno, considerando solo l'intervallo richiesto.
    for item in time_series:
        if not isinstance(item, list) or len(item) < 2:
            raise ExamException("Errore, serie temporale non valida")

        timestamp = item[0]
        passengers = item[1]

        if not isinstance(timestamp, str) or len(timestamp) < 4:
            raise ExamException("Errore, timestamp non valido nella serie temporale")

        if not isinstance(passengers, int):
            raise ExamException("Errore, valore passeggeri non valido nella serie temporale")

        year = timestamp[:4]

        if first_year <= year <= last_year:
            if year not in passengers_by_year:
                passengers_by_year[year] = []

            passengers_by_year[year].append(passengers)

    if first_year not in passengers_by_year or last_year not in passengers_by_year:
        raise ExamException("Errore, gli estremi dell'intervallo non sono presenti nei dati")

    average_by_year = {}

    # Calcolo la media usando solo i mesi disponibili per ogni anno.
    for year, passengers in passengers_by_year.items():
        average_by_year[year] = sum(passengers) / len(passengers)

    variations = {}
    years = sorted(average_by_year.keys())

    # Calcolo le differenze tra anni consecutivi disponibili.
    for index in range(1, len(years)):
        previous_year = years[index - 1]
        current_year = years[index]
        key = "{}-{}".format(previous_year, current_year)
        variations[key] = average_by_year[current_year] - average_by_year[previous_year]

    return variations


def _is_valid_year(year):
    return isinstance(year, str) and len(year) == 4 and year.isdigit()


if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_folder, "data", "data.csv")

    time_series_file = CSVTimeSeriesFile(name=data_file)
    time_series = time_series_file.get_data()
    variations = compute_variations(time_series, "1949", "1951")
    print(variations)
