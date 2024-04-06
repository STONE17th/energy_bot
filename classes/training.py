class Training:
    def __init__(self, data: tuple):
        self.id = data[0]
        self.athlete = AthletesDB().load_by_id(int(data[1]))
        self.date = data[2]
        self.message = data[3]

    def for_message(self):
        return f'{self.date}\n{self.message}\n'

    def __repr__(self):
        return f'{self.date} - {self.message}'