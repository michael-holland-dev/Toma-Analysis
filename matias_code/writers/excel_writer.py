from file_writer import FileWriter

class ExcelWriter(FileWriter):
    def __init__(self):
        super().__init__()

    def write(self):
        self._create_dataframe()

        super().write()


if __name__ == "__main__":
    writer = ExcelWriter()

    writer.write()