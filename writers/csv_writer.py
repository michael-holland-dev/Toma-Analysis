from file_writer import FileWriter

class CSVWriter(FileWriter):
    def __init__(self):
        super().__init__()

    def write(self):
        self._create_dataframe()

        self.file_path


if __name__ == "__main__":
    writer = CSVWriter()

    writer.write()