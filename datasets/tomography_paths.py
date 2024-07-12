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
        return {
                "data": self.fpaths[index]
            }
    

if __name__ == "__main__":
    paths = TomographyPaths("/home/mwh1998/fsl_groups/", 10)
    print(paths[0])