from writers import get_writer
from analyzers import get_analysis
from datasets import TomographyPaths
from utils import Processor, Checkpointer
import argparse

def parse_arguments():
    
    L_PATHS = ["/home/matiasgp/groups/grp_tomo_db1_d1/nobackup/archive/TomoDB1_d1/FlagellarMotor_P1", 
                    "/home/matiasgp/groups/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2", 
                    "/home/matiasgp/groups/grp_tomo_db1_d3/nobackup/archive/TomoDB1_d3", 
                    "/home/matiasgp/groups/grp_tomo_db1_d4/nobackup/archive/TomoDB1_d4"
                ]
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", "-i", type=str, default=L_PATHS, help="Filepath that contains the tomographies.")
    parser.add_argument("--max-files", "-mf", type=int, default=None, help="Maximum number of files to read in.")
    parser.add_argument("--output_path", "-o", type=str, default="./output", help="Output folder to save the csv with the statistics.")
    parser.add_argument("--writer-type", "-fw", type=str, default="csv", help="The type of writer to choose from, options currently include csv and xlsx.")
    parser.add_argument("--analysis-type", "-at", type=str, default="basic", help="The type of analysis to conduct.")
    parser.add_argument("--batch-size", "-bs", type=int, default=100, help="The number of items in a batch to submit to the multi-threading.")
    parser.add_argument("--checkpoint", "-c", action="store_true", default=False, help="Signal checkpointing flag.")
    
    try:
        args = parser.parse_args()
        return args.__dict__
    except argparse.ArgumentError as e:
        # Handle argument errors
        print(f'Argument error: {e}')
        parser.print_usage()
    except Exception as e:
        # Handle any other exceptions that occur during processing
        print(f'Unexpected error: {e}')
        parser.print_usage()

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