import subprocess  # Import subprocess for running shell commands
from tqdm import trange  # Import trange from tqdm for progress bar
from .threading_manager import thread  # Import thread function from threading_manager module
import random  # Import random for sampling

def get_sample_list(files_list: list, sample_size: int):
    """
    Get a random sample of the specified size from the list of files.
    
    Parameters:
    files_list (list): List of files to sample from.
    sample_size (int): The number of files to sample.
    
    Returns:
    list: A random sample of files.
    """
    return random.sample(files_list, sample_size)

def recParseThroughDir(root_paths: list, sample: bool = False, sample_size: int = 100) -> list:
    """
    Get the list of .rec files in the directory, optionally sampling from them.
    
    Parameters:
    root_paths (list): List of root paths to search for .rec files.
    sample (bool): Whether to sample the results.
    sample_size (int): The number of samples to return if sampling is enabled.
    
    Returns:
    list: A list of .rec files found in the specified directories.
    """
    clean_results = []  # List to store clean results
    for path in root_paths:
        # Run the lfs find command to locate .rec files
        result = subprocess.run(["lfs", "find", path, "-type", "f", "--name", "*.rec"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                check=True) 
        # Process the output of the command
        for name in result.stdout.splitlines():
            components = name.split('/')
            found_peet = False
            for component in components:
                if 'peet' in component.lower() or "align" in component.lower():
                    found_peet = True
            if not found_peet:
                clean_results.append(name)
    
    # Optionally sample the results
    if sample:
        clean_results = get_sample_list(clean_results, sample_size)
        
    """*******FOR TEST ONLY*******"""
    clean_results = ["/home/matiasgp/groups/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/legionella/dg2017-02-01-8/JV1181_010220170008_SIRT_1k.rec"]
    """*******END OF TEST*******"""
    return clean_results

def task_batcher(
        root_paths: list,
        batch_size: int,
        thread: callable,
        analyzer_task: callable,
        writer,
        sample=False,
        sample_size: int = 100
    ):
    """
    Batch process .rec files by analyzing them in parallel and writing the results.
    
    Parameters:
    root_paths (list): List of root paths to search for .rec files.
    batch_size (int): Number of files to process in each batch.
    thread (callable): Function to process a batch of files in parallel.
    analyzer_task (callable): Task to be performed on each file.
    writer: Writer object to save the results.
    sample (bool): Whether to sample the results.
    sample_size (int): The number of samples to return if sampling is enabled.
    """
    
    # Get the list of paths to process
    paths = recParseThroughDir(root_paths, sample, sample_size)
    
    # Process paths in batches
    for i in trange(0, len(paths), batch_size, desc='Patience, your tomograms are being analyzed'):
        batch = paths[i:i + batch_size]
        results = thread(batch, analyzer_task)
    
        """Call writers"""
        writer.write_open()  # Open the writer
        writer.write_rows(results)  # Write the results
        writer.close  # Close the writer
        """End of writers"""

# Comments added by ChatGPT

    
    