class ExamException(Exception):
    pass


class MovingAverage:
    def __init__(self, window_length):
        if not isinstance(window_length, int) or window_length <= 0:
            raise ExamException("Errore, la lunghezza della finestra deve essere un intero positivo")

        self.window_length = window_length

    def compute(self, data):
        if not isinstance(data, list):
            raise ExamException("Errore, i dati devono essere contenuti in una lista")

        if len(data) < self.window_length:
            raise ExamException("Errore, la lista contiene meno elementi della finestra")

        for value in data:
            if not isinstance(value, (int, float)):
                raise ExamException("Errore, tutti gli elementi della lista devono essere numeri")

        moving_averages = []

        for index in range(len(data) - self.window_length + 1):
            window = data[index:index + self.window_length]
            average = sum(window) / self.window_length
            moving_averages.append(average)

        return moving_averages


if __name__ == "__main__":
    moving_average = MovingAverage(2)
    result = moving_average.compute([2, 4, 8, 16])
    print(result)
