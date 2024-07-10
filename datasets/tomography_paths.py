from datasets.dataset_base import Dataset
from typing import SupportsIndex

class TomographyPaths(Dataset):
    def __init__(
            self,
            input_path,
            max_files
        ):
        super().__init__(
            input_path,
        )

    def __len__(self):
        return len(self.fpaths)
    
    def pop(
            self,
            index: SupportsIndex = -1
        ):
        return self.fpaths.pop(index)
    
    def __getitem__(self, index):
        return self.fpaths[index]