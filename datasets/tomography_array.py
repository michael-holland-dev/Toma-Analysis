from datasets.tomography_paths import Dataset
import numpy as np
import mrcfile
import random 

class TomographyArray(Dataset):
    def __init__(self,
                 data_folder_path: list, 
                 max_files: int = None
                 ):
        super().__init__(data_folder_path,
                         max_files
                         )
        self.current_idx = 0
        self.height = None
        self.bacteria_name = None

    def __getitem__(self, idx):
            if idx >= len(self.fpaths) or idx < 0:
                raise IndexError("Index out of range")

            with mrcfile.open(self.fpaths[idx]) as mrc:
                tomogram = mrc.data.copy()

            # height = tomogram.shape[0]
            # margin = int(height * 0.2)
            # tomogram = tomogram[margin:(height - margin), :, :]
            
            bacteria_name = self.fpaths[idx].split("/")[-1].split(".")[0]
            
            return {
                "key": self.fpaths[idx],
                "data": tomogram,
                "bacteria_name": bacteria_name
            }

    def __len__(self):
        return len(self.fpaths)

    def pop(self):
        if self.current_idx >= len(self.fpaths):
            raise IndexError("Index out of range in pop()")

        result = self.__getitem__(self.current_idx)
        self.current_idx += 1
        return result

    def random_pop(self):
        if len(self.fpaths) == 0:
            raise IndexError("No files available for random_pop()")

        idx = random.randint(0, len(self.fpaths) - 1)
        return self.__getitem__(idx)