import os
from abc import ABC, abstractmethod

class Dataset(ABC):
    def __init__(
            self,
            data_folder_path: str,
            max_files: int=None,
        ):

        # Set the max files variable. If it's none, then have it be 
        self.max_files = max_files if max_files is not None else float('inf')

        # Have it search for all of the .mrc files
        self.fpaths = []
        path, root_folders, _ = next(os.walk(data_folder_path))
        root_folders.remove("fslg_documents")

        for folder in root_folders:
            # Recursively search through all of the data directories for the .mrc files
            self.__data_folder_path_helper(path, folder)

    def __data_folder_path_helper(self, fpath, top_folder):
        cwd = os.path.join(fpath, top_folder)
        path, folders, files = next(os.walk(cwd))

        for file in files:
            if ".rec" in file:
                self.fpaths.append(os.path.join(cwd, file))

        if len(self.fpaths) < self.max_files:
            for folder in folders:
                # Makes sure that the folder isn't a hidden folder.
                if folder[0] != ".":
                    self.__data_folder_path_helper(path, folder)
    
    @abstractmethod
    def __len__(self):
        pass
    
    @abstractmethod
    def pop(self):
        pass

        