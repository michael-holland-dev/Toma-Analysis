
class FileWriter:
    def __init__(self):
        self.file_path = "./myfile.csv"
        print("Test")

    def _create_dataframe(self):
        print("Created_Dataframe")

if __name__ == "__main__":
    writer = FileWriter()