from datasets import TomographyPaths

path_dataset = TomographyPaths("/home/mwh1998/fsl_groups/", max_files=10)

print(path_dataset.get_sample_list(10))