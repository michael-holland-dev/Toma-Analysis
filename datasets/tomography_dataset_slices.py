from datasets.tomography_paths import Dataset
import numpy as np
import mrcfile

class TomographyDatasetSlices(Dataset):
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
        
        #Eliminate top and bottom of the tomogram
        margin = int(self.height * 0.2)
        self.tomogram = self.tomogram[margin:(self.height - margin), :, :]
        
        # Extract the middle slice
        middle_slice = self.tomogram[int(self.height/2)-5:int(self.height/2)+5, :, :].mean(0)
        
        # Get bacteria name from path
        self.bacteria_name = self.fpaths[idx].split("/")[-1].split(".")[0]
        
        self.current_idx += 1
        
        return {
            "key": self.bacteria_name,
            "data": middle_slice,
        }
        

    def __len__(self):
        return len(self.fpaths) - self.current_idx
    
    def pop(self) -> dict:
        return self.__getitem__()

