from abc import ABC, abstractmethod

class Writer(ABC):
    def __init__(self):
        self.file_path = "./myfile.csv"
        print("Test")

    def _create_dataframe(self):
        print("Created_Dataframe")

    @abstractmethod
    def write_batch(
            self,
            batch_results,
            **kwargs
        ):
        pass

if __name__ == "__main__":
    writer = Writer()