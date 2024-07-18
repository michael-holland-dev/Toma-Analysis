from analyzers import Analysis
import numpy as np                 # Import numpy for array operations
import os.path                     # Import os for operating system functions


class TomoStats(Analysis):
    def analyze(self, numpy_array, results, filepath, **kwargs):
        
        try:    
            d_shp = numpy_array.shape             # Get shape of the numpy array
            min_val = np.min(numpy_array)         # Calculate minimum value in array
            max_val = np.max(numpy_array)         # Calculate maximum value in array
            mean = np.mean(numpy_array)           # Calculate mean value of array
            
            # Find the name of the bacteria
            #b_name = find_bacteria_name(file)
            
            # Check if tomogram is a sirt tomogram
            #sirt = is_sirt(file)
            
            # Prepare result
            # result = [filepath, b_name[0], os.path.basename(filepath), d_shp, mean, min_val, max_val, sirt]
            result = [filepath, os.path.basename(filepath), d_shp, mean, min_val, max_val]
            
            """Plots here"""
            
            """End of test"""
            
            # Update a shared thread data by adding results to queue
            results.append({filepath: result})
                    
        except Exception as e:
            # Handle any exceptions that occur during processing
            print(f'Error processing {filepath}: {e}')
        
