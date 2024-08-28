from analyzers import Analysis
import numpy as np                 # Import numpy for array operations
import os.path                     # Import os for operating system functions
from scipy.stats import entropy
import sympy as sp
from scipy.ndimage import label

class IntensitySegmenter(Analysis):
    def __init__(self):
        pass
    
    def analyze(self, data, key, results: dict, **kwargs):
        try:
            
            data = min_max_normalize(data) 
            data = histogram_equalization_3d(data)
    
            # Extract the base name (file name with extension)
            base_name = os.path.basename(key)
            # Remove the .rec extension
            base_name = os.path.splitext(base_name)[0]
        
            
            print(f'Done with {key}')
            
            seg_results = {
                "means": means,
                
            }
            results[key] = seg_results
                    
        except Exception as e:
            # Handle any exceptions that occur during processing
            print(f'Error processing {key}: {e}')
            
def min_max_normalize(array):
    # Convert to float32 to prevent overflow issues
    array = array.astype(np.float32)
    
    min_val = np.min(array)
    max_val = np.max(array)
    
    if min_val == max_val:
        # Avoid division by zero if the array contains a single unique value
        return np.zeros(array.shape, dtype=np.float32)
    
    normalized_array = (array - min_val) / (max_val - min_val)
    return normalized_array


def histogram_equalization_3d(image):
    """
    Apply histogram equalization to a 3D array.
    
    Args:
    - image (np.ndarray): 3D array representing the image or volume.
    
    Returns:
    - image_equalized (np.ndarray): Histogram-equalized 3D array.
    """
    # Flatten the 3D image array and calculate histogram
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 1])

    # Calculate cumulative distribution function (CDF)
    cdf = hist.cumsum()
    cdf_normalized = cdf / cdf.max()  # Normalize CDF

    # Use linear interpolation of the CDF to find new pixel values
    image_equalized = np.interp(image.flatten(), bins[:-1], cdf_normalized)

    # Reshape the flattened image back to the original 3D shape
    image_equalized = image_equalized.reshape(image.shape)
    
    return image_equalized

def select_ranked_dark_group(array_3d, percentile=20, rank=1, connectivity=2):
    """
    Normalizes the 3D array, then selects a specific group of dark values based on size ranking.

    Parameters:
        array_3d (np.ndarray): The input 3D array.
        percentile (float): The percentile below which values are considered dark, after normalization.
        rank (int): The rank of the group to return based on size (1 for largest, 2 for second largest, etc.).
        connectivity (int): The connectivity criterion (1 for direct neighbors, 2 for diagonal neighbors).

    Returns:
        ranked_group_mask (np.ndarray): A binary mask of the same shape as array_3d, where the ranked dark group is marked as 1.
        ranked_group_size (int): The size of the ranked dark group.
        normalized_array (np.ndarray): The normalized array with values in the range [0, 1].
    """
    # Normalize the array to the range [0, 1]
    array_min = np.min(array_3d)
    array_max = np.max(array_3d)
    
    # Prevent division by zero in case all values are the same
    if array_max - array_min != 0:
        normalized_array = (array_3d - array_min) / (array_max - array_min)
    else:
        normalized_array = np.zeros_like(array_3d)

    # Calculate the dynamic threshold based on the specified percentile
    threshold = np.percentile(normalized_array, percentile)

    # Create a binary mask where normalized values below the threshold are marked as 1, others as 0
    dark_values_mask = normalized_array < threshold

    # Label connected components in the binary mask
    labeled_array, num_features = label(dark_values_mask, structure=np.ones((3, 3, 3)) if connectivity == 2 else None)

    if num_features == 0:
        print("No dark-value groups found.")
        return np.zeros_like(array_3d), 0, normalized_array  # Return an empty mask if no groups are found

    # Find all group sizes by counting occurrences of each label
    label_counts = np.bincount(labeled_array.flat)

    # Exclude the background label (index 0) and sort groups by size in descending order
    sorted_labels_and_sizes = sorted(enumerate(label_counts[1:], start=1), key=lambda x: x[1], reverse=True)

    if rank > len(sorted_labels_and_sizes):
        print(f"Rank {rank} exceeds the number of detected groups. Returning an empty mask.")
        return np.zeros_like(array_3d), 0, normalized_array  # Return an empty mask if rank is out of bounds

    # Get the label for the specified rank
    ranked_group_label, ranked_group_size = sorted_labels_and_sizes[rank - 1]

    # Create a mask for the ranked group
    ranked_group_mask = labeled_array == ranked_group_label

    return ranked_group_mask, ranked_group_size, normalized_array

def fit_and_normalize_index(numbers, degree=10):
    """
    Fit a polynomial to the data using normalized indices as x-coordinates
    and normalize the y-values as well.

    Parameters:
    - numbers: list of y-values to fit
    - degree: degree of the polynomial to fit

    Returns:
    - normalized_polynomial: polynomial function with normalized x (as a sympy expression)
    - normalized_x: normalized x-values
    - normalized_y: normalized y-values
    """
    # Generate the index values (independent variable)
    x = np.arange(len(numbers))
    y = np.array(numbers)

    # Normalize the index values to the range [0, 1]
    normalized_x = (x - x.min()) / (x.max() - x.min())

    # Normalize the y-values to the range [0, 1]
    normalized_y = (y - y.min()) / (y.max() - y.min())

    # Fit a polynomial of the specified degree using numpy
    coefficients = np.polyfit(normalized_x, normalized_y, degree)
    
    # Convert coefficients to sympy expression
    x_sym = sp.symbols('x')
    normalized_polynomial = sum(c * x_sym**i for i, c in enumerate(reversed(coefficients)))
    
    normalized_polynomial = str(normalized_polynomial)
    
    return normalized_polynomial


