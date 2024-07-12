
class FileWriter:
    def __init__(self, filename):
        self.file_path = "./myfile.csv"
        

    def _create_dataframe(self, first_row):
        self.first_row = first_row
        

if __name__ == "__main__":
    writer = FileWriter()