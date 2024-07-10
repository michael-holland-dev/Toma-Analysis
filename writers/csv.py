from writers import Writer

class CSV(Writer):
    def __init__(self, output_path):
        super().__init__()

    def write(self):
        self._create_dataframe()
        self.file_path


if __name__ == "__main__":
    writer = CSV()

    writer.write()