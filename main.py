from writers import get_writer
from analyzers import get_analysis
from datasets import TomographyPaths
from utils import Processor, Checkpointer
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, default="./input.csv", help="Filepath that contains the tomographies.")
    parser.add_argument("--max-files", "-mf", type=int, default=None, help="Maximum number of files to read in.")
    parser.add_argument("--output", "-o", type=str, default="./output", help="Output folder to save the csv with the statistics.")
    parser.add_argument("--writer-type", "-fw", type=str, default="csv", help="The type of writer to choose from, options currently include csv and xlsx.")
    parser.add_argument("--analysis-type", "-at", type=str, default="base", help="The type of analysis to conduct.")
    parser.add_argument("--batch-size", "-bs", type=int, default=100, help="The number of items in a batch to submit to the multi-threading.")
    parser.add_argument("--checkpoint", "-c", action="store_true", default=False, help="Signal checkpointing flag.")
    args = parser.parse_args()

    return args.__dict__

def main(
    input_path: str,
    max_files: int = None,
    output_path: str = "./output",
    writer_type: str = "csv",
    analysis_type: str = "basic",
    batch_size: int = 100,
    checkpoint: bool = False,
    checkpoint_interval: int = 5
):
    print(checkpoint)
    # Retrieve Specified Dependencies
    writer = get_writer(writer_type)(output_path)
    analyzer = get_analysis(analysis_type)()
    checkpointer = Checkpointer(output_path, checkpoint_interval) if checkpoint else None
    
    processor = Processor(
        analyzer,
        writer,
        batch_size,
        checkpointer
    )

    data = TomographyPaths(
        input_path,
        max_files
    )
    processor.process_data(data)


if __name__ == "__main__":
    args = parse_arguments()
    main(**args)