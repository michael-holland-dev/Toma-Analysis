from writers import Writer
import pandas as pd
import os

class CSV(Writer):
    def __init__(self, output_file):
        super().__init__()

    def write(self, batch_results):
        df = pd.DataFrame(batch_results)
        
        if os.path.exists(self.file_path):
            prior_set = pd.read_csv(self.file_path)
            df = pd.concat([df, prior_set])

        df.to_csv(self.file_path, index=False)
    
    def write_rows(self, data: dict):
        """
        Write multiple rows of data to the CSV file using pandas.

        Args:
        - data (dict): Dictionary where keys are row identifiers and values are lists representing rows of data.
        """
        df = pd.DataFrame.from_dict(data, orient='index')
        df.to_csv(self.file_path, mode='a', header=False)

    def close(self):
        """
        Close the CSV file.
        """
        self.file.close()  # Close the CSV file
    
    


if __name__ == "__main__":
    writer = CSV()

    writer.write()