from analyzers import Analysis
import numpy as np                 # Import numpy for array operations
import os.path                     # Import os for operating system functions
from writers import Slide, Video

class TomoStats(Analysis):
    def __init__(self):
        pass
    
    def analyze(self, data, key, results: dict, **kwargs):
        try:
            data = normalize_standardization(data) 
            d_shp = data.shape  # Get shape of the numpy array
            min_val = np.min(data)  # Calculate minimum value in array
            max_val = np.max(data)  # Calculate maximum value in array
            mean = np.mean(data)  # Calculate mean value of array
            
            # Extract the base name (file name with extension)
            base_name = os.path.basename(key)
            # Remove the .rec extension
            base_name = os.path.splitext(base_name)[0]

        
            """Plot Video test"""
            test_plot = Video(data, str(base_name))
            test_plot.plot_video(20, d_shp[0], 15, 0)
            test_plot = Video(data, str(base_name))
            test_plot.plot_video(20, d_shp[1], 15, 1)
            test_plot = Video(data, str(base_name))
            test_plot.plot_video(20, d_shp[2], 15, 2)
            """End of test"""
            
            """Plot Image Test"""
            test_plot = Slide(data, str("/home/matiasgp/Desktop/Toma-Analysis/tests/"+base_name+".png"))
            test_plot.plot_3d_img(1, int(d_shp[1]/2))
            test_plot = Slide(data, str("/home/matiasgp/Desktop/Toma-Analysis/tests/"+"normalized_"+base_name+".png"))
            test_plot.plot_3d_img(1, int(d_shp[1]/2))
            """End of test"""
            
            seg_results = {
                "shape": d_shp,
                "mean": mean,
                "min_val": min_val,
                "max_val": max_val,
                
            }
            results[key] = seg_results
                    
        except Exception as e:
            # Handle any exceptions that occur during processing
            print(f'Error processing {key}: {e}')
            
def normalize_min_max(arr):
    # Ensure array is in floating point format for division
    arr = arr.astype(np.float32)
    
    # Compute min and max
    min_val = arr.min()
    max_val = arr.max()
    
    # Perform normalization
    arr = (arr - min_val) / (max_val - min_val)
    
    return arr

import numpy as np

def normalize_standardization(arr):
    # Ensure array is in floating point format for division
    arr = arr.astype(np.float32)
    
    # Compute mean and standard deviation
    mean = arr.mean()
    std = arr.std()
    
    # Avoid division by zero
    std = np.where(std == 0, 1, std)
    
    # Perform normalization
    arr = (arr - mean) / std
    
    return arr
