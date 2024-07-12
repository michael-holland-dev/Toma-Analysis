from writers import Writer
import pandas as pd
import os

class CSV(Writer):
    def __init__(self, output_file):
        super().__init__()

    def write(self, batch_results):
        df = pd.DataFrame(batch_results)
        
        if os.path.exists(self.file_path):
            prior_set = pd.read_csv(df)

            df = pd.concat([df, prior_set])

        df.to_csv(self.file_path)
    
    


if __name__ == "__main__":
    writer = CSV()

    writer.write()