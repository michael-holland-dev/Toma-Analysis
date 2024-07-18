from datasets.tomography_paths import Dataset
import numpy as np
import mrcfile

class TomographySlices(Dataset):
    def __init__(
            self,
            file_path: str,
            num_to_test
        ):
        self.num_to_test = num_to_test
        self.tomogram = None

        with mrcfile.open(file_path) as mrc:
            self.tomogram = mrc.data.copy()

        height = self.tomogram.shape[0]
        margin = int(height * .2)
        self.bacteria_name = file_path.split("/")[-1].split(".")[0]

        self.tomogram = self.tomogram[margin:(height-margin), :, :]

    def __getitem__(self, _=None) -> dict:
        idx = np.random.randint(0, self.tomogram.shape[0]-5)
        selected_slice = self.tomogram[idx-2:idx + 2, :, :].mean(0)
        return {
            "key": self.num_to_test,
            "data": selected_slice,
            "idx": idx
        }

    def __len__(self):
        return self.num_to_test
    
    def pop(self) -> dict:
        self.num_to_test -= 1
        return self.__getitem__()

