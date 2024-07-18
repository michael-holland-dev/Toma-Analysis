from plotters import Slide, Video  # Import custom plotting classes
from queue import Queue            # Import Queue for storing results
import numpy as np                 # Import numpy for array operations
import mrcfile                     # Import mrcfile for MRC file handling
import threading                   # Import threading for concurrent processing
import difflib                     # Import difflib for sequence matching
import os                          # Import os for operating system functions
from writers import CSVWriter

def numpy_analysis(file:str, results_queue: Queue):
    """
    Process an REC file to extract data and perform analysis.
    
    Args:
    - file: File path of the MRC file to process.
    - results_queue: Queue to store processed results.
    """
    try:
        # Process each file
        numpy_array = convert_to_numpy(file)  # Convert rec file to numpy array
        d_shp = numpy_array.shape             # Get shape of the numpy array
        min_val = np.min(numpy_array)         # Calculate minimum value in array
        max_val = np.max(numpy_array)         # Calculate maximum value in array
        mean = np.mean(numpy_array)           # Calculate mean value of array
        
        # Find the name of the bacteria
        b_name = find_bacteria_name(file)
        
        # Check if tomogram is a sirt tomogram
        sirt = is_sirt(file)
        
        # Prepare initial result with basic information
        result = [file, b_name[0], os.path.basename(file), d_shp, mean, min_val, max_val, sirt]
        
        # Normalize the numpy array between 0 and 1 and run analysis on it
        n_numpy_array = normalize_numpy(numpy_array)
        
        # Extract normalized data statistics
        n_d_shp = n_numpy_array.shape
        n_min_val = np.min(n_numpy_array)
        n_max_val = np.max(n_numpy_array)
        n_mean = np.mean(n_numpy_array)
        
        name = os.path.basename(file).split(".")[0]
        
        wr = CSVWriter("/home/matiasgp/Desktop/Toma-Analysis/tests/normalized_"+name+".csv", [name])
        """Plot Video test"""
        test_plot = Video(n_numpy_array, str(name+"0"))
        test_plot.plot_video(20, n_d_shp[0], 5, 0, wr)
        test_plot = Video(n_numpy_array, str(name+"1"))
        test_plot.plot_video(20, n_d_shp[1], 15, 1, wr)
        test_plot = Video(n_numpy_array, str(name+"2"))
        test_plot.plot_video(20, n_d_shp[2], 15, 2, wr)
        """End of test"""
        
        """Plot Image Test"""
        test_plot = Slide(numpy_array, str("/home/matiasgp/Desktop/Toma-Analysis/tests/"+name+".png"))
        test_plot.plot_3d_img(1, int(d_shp[1]/2))
        test_plot = Slide(n_numpy_array, str("/home/matiasgp/Desktop/Toma-Analysis/tests/"+"normalized_"+name+".png"))
        test_plot.plot_3d_img(1, int(n_d_shp[1]/2))
        """End of test"""
        
        # Prepare normalized result for final output
        normalized_result = [n_d_shp, n_mean, n_min_val, n_max_val, sirt]
        
        # Update a shared thread data by adding results to queue
        results_queue.put((file, result + normalized_result))
                
    except Exception as e:
        # Handle any exceptions that occur during processing
        print(f'Error processing {file}: {e}')
        
# Function to convert MRC file to numpy array
def convert_to_numpy(file_path: str):
    """
    Read a .rec file and convert it to a NumPy array.
    
    Args:
    - file_path: File path of the .rec file.
    
    Returns:
    - numpy.ndarray or None: NumPy array containing the data from the .rec file,
      or None if there was an error.
    """
    
    with mrcfile.open(file_path, permissive=True) as mrc:

        array = mrc.data
        #array = array.astype(np.float64)
        return array
    

# Function to check if file path indicates a SIRT tomogram
def is_sirt(file: str):
    """
    Check if the file path indicates a SIRT tomogram.
    
    Args:
    - file: File path of the tomogram file.
    
    Returns:
    - bool: True if "sirt" is in the file name, False otherwise.
    """
    if 'sirt' in os.path.basename(file).lower():
        return True
    else:
        return False

# Function to find the name of bacteria from the file path
def find_bacteria_name(path):
    """
    Find the name of bacteria from the file path.
    
    Args:
    - path: File path containing information about the bacteria.
    
    Returns:
    - list: List of possible names of bacteria found in the file path.
    """
    possibilities = read_file_to_list("/home/matiasgp/Desktop/Toma-Analysis/analyzers/cleaned_titles_input.txt")
    words = []
    for w in path.split("/"):
        # Use difflib to find close matches of path components in possibilities
        if len(difflib.get_close_matches(w, possibilities, n=1, cutoff=0.51)) != 0:
            words.append(w)
    if len(words) == 0:
        # If no matches found, attempt to retrieve name from specific path components
        words = path.split("/")[9]
        if "tomodb1_d4" in path.split("/")[7].lower:
            words = path.split("/")[8]
    return words

# Function to read lines from a file and return them as a list
def read_file_to_list(input_file):
    """
    Read lines from a file and return them as a list.
    
    Args:
    - input_file: File path of the input file to read.
    
    Returns:
    - list: List containing lines read from the input file.
    """
    
    return lines

# Function to normalize numpy array between 0 and 1
def normalize_numpy(data):
    """
    Normalize the input numpy array between 0 and 1.
    
    Args:
    - data: Input numpy array to be normalized.
    
    Returns:
    - numpy.ndarray: Normalized numpy array with values between 0 and 1.
    """
    # Ensure the array is of type float32
    data = data.astype(np.float32)
    print("processed")

    # Step 1: Compute the logarithmic scaling
    log_min = np.min(np.log1p(np.abs(data)))
    log_max = np.max(np.log1p(np.abs(data)))
    
    

    # Handle cases where log_min and log_max are too large/small
    if log_min == log_max:
        data_normalized = np.zeros_like(data)
    else:
        # Step 2: Apply the log transformation
        data_log_transformed = np.log1p(np.abs(data))

        # Step 3: Normalize the log-transformed data
        data_normalized = (data_log_transformed - log_min) / (log_max - log_min)

        # Step 4: Restore the sign of the original data
        data_normalized *= np.sign(data)
        
    return data_normalized

# Comments added by ChatGPT
