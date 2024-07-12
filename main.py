from writers import get_writer
from analyzers import get_analysis
from datasets import TomographyPaths
from utils import Processor, Checkpointer
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", "-i", type=str, default="./input.csv", help="Filepath that contains the tomographies.")
    parser.add_argument("--max-files", "-mf", type=int, default=None, help="Maximum number of files to read in.")
    parser.add_argument("--output-path", "-o", type=str, default="./output", help="Output folder to save the csv with the statistics.")
    parser.add_argument("--writer-type", "-fw", type=str, default="csv", help="The type of writer to choose from, options currently include csv and xlsx.")
    parser.add_argument("--analysis-type", "-at", type=str, default="base", help="The type of analysis to conduct.")
    parser.add_argument("--batch-size", "-bs", type=int, default=100, help="The number of items in a batch to submit to the multi-threading.")
    parser.add_argument("--checkpoint", "-c", action="store_true", default=False, help="Signal checkpointing flag.")
    parser.add_argument("--checkpoint-interval", "-ci", type=int, default=5, help="Number of batches per checkpoint")
    args = parser.parse_args()

    return args.__dict__

def main(
    input_path: str,
    max_files: int = None,
    output_path: str = "./output",
    writer_type: str = "csv",
    analysis_type: str = "base",
    batch_size: int = 100,
    checkpoint: bool = False,
    checkpoint_interval: int = 5
):
    print("Starting Analysis...")
    input_path = "/home/mwh1998/fsl_groups/"

    # Retrieve Specified Dependencies
    print("Setting up writer...")
    writer = get_writer(writer_type)(output_path)

    print("Setting up analysis...")
    analyzer = get_analysis(analysis_type)()

    checkpointer = None
    if checkpoint:
        print("Checkpoint flag received, setting up checkpointer...")
        checkpointer = Checkpointer(output_path, checkpoint_interval)
    
    print("Configuring Processor...")
    processor = Processor(
        analyzer,
        writer,
        batch_size,
        checkpointer
    )

    print("Compiling Dataset...") 
    data = TomographyPaths(
        input_path,
        max_files
    )

    print("Processing Data Now...")
    processor.process_data(data)


if __name__ == "__main__":
    args = parse_arguments()
    main(**args)