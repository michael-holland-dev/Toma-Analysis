from writers import SegmentationSaver
from analyzers import BacteriaSegmenter
from datasets import TomographySlices
from utils.data_factory import DataFactory
import torch
import os

def main():
    print("Compiling Dataset...")
    
    # Sets up a tomography to pull slices
    data = TomographySlices(
        os.environ["TOMOGRAM_FPATH"],
        100
    )

    print("Setting up Analysis Pipeline...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    analyzer = BacteriaSegmenter(device=device)

    print("Setting up Writer...")
    writer = SegmentationSaver(data.bacteria_name)
    
    print("Configuring Processor...")
    batch_size = 1
    data_factory = DataFactory(
        analyzer,
        writer,
        batch_size
    )

    print("Processing Data...")
    data_factory.process(data)


if __name__ == "__main__":
    main()