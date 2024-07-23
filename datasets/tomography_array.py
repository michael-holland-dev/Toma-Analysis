from datasets.tomography_paths import Dataset
import numpy as np
import mrcfile

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

    def __getitem__(self, _=None) -> dict:
        idx = self.current_idx
        self.tomogram = None
        with mrcfile.open(self.fpaths[idx]) as mrc:
            self.tomogram = mrc.data.copy()
        self.height = self.tomogram.shape[0]
        margin = int(self.height * 0.2)
        self.bacteria_name = self.fpaths[idx].split("/")[-1].split(".")[0]
        self.tomogram = self.tomogram[margin:(self.height - margin), :, :]
        self.current_idx += 1
        return {
            "key": self.fpaths[idx],
            "data": self.tomogram,
        }
        

    def __len__(self):
        return len(self.fpaths) - self.current_idx
    
    def pop(self) -> dict:
        return self.__getitem__()

