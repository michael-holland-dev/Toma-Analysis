import matplotlib.pyplot as plt
from plotters.img_plotter import Slide
import numpy as np
import imageio as iio
import os
from writers import CSVWriter

class Video(Slide):
    def __init__(self, numpy_array, output_name):
        """
        Initialize the Video object by calling the parent Slide class constructor.
        
        Parameters:
        numpy_array (numpy.ndarray): The 3D numpy array representing the image data.
        output_name (str): The name of the output video file.
        """
        super().__init__(numpy_array, output_name)
        
    def plot_video(self, initial_slice, final_slice, slices_per_frame, axis, save_path):
        """
        Create a video from a series of 2D slices of the 3D numpy array.
        
        Parameters:
        initial_slice (int): The starting index for slicing.
        final_slice (int): The ending index for slicing.
        slices_per_frame (int): The number of slices to average per frame.
        axis (int): The axis along which to take the slices (0, 1, or 2).
        """
        filenames = []  # List to store temporary filenames
        listofmeans = [] # List to store temporary means

        for start in range(initial_slice, final_slice, slices_per_frame):
            end = min(start + slices_per_frame, final_slice)
            xlabel, ylabel = "", ""
            
            # Calculate the average of the slices along the specified axis
            if axis == 0:
                slice_data = np.mean(self.numpy_array[start:end, :, :], axis=0)
                xlabel, ylabel = 'Y axis', 'Z axis'
            elif axis == 1:
                slice_data = np.mean(self.numpy_array[:, start:end, :], axis=1)
                xlabel, ylabel = 'X axis', 'Z axis'
            elif axis == 2:
                slice_data = np.mean(self.numpy_array[:, :, start:end], axis=2)
                xlabel, ylabel = 'X axis', 'Y axis'
            else:
                raise ValueError("Axis must be 0, 1, or 2")
            
            # Create a temporary file to save the plot
            temp_filename = f'temp_slice_{start}_{end}_{self.outputname}.png'
            temp = Slide(slice_data, temp_filename)
            listofmeans.append(temp.plot_2d_img(axis, start, xlabel, ylabel))
            filenames.append(temp_filename)
        
        # Create a video from the saved images
        with iio.get_writer(save_path, mode='I', fps=4) as writer:
            print("Creating Video")
            for filename in filenames:
                image = iio.imread(filename)
                writer.append_data(image)
                
        # Create a plot with the means through time
        # plot_bar_chart(data=listofmeans, title=self.outputname, ylabel="Mean")
        
        # Clean up temporary files
        for filename in filenames:
            os.remove(filename)

# Comments added by ChatGPT
def plot_bar_chart(data, title='Bar Chart', xlabel='Slice', ylabel='Value'):
    """
    Plots a bar chart of the given list of numbers and saves it with the title as the filename.

    Parameters:
    - data: list of numbers to plot the bar chart for.
    - title: title of the bar chart (default is 'Bar Chart').
    - xlabel: label for the x-axis (default is 'Index').
    - ylabel: label for the y-axis (default is 'Value').
    """
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(data)), data, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Save the plot with the title as the filename
    # Replace spaces in title with underscores and add .png extension
    filename = "/home/matiasgp/Desktop/Toma-Analysis/tests/hist_" + title.replace(' ', '_') + '.png'
    plt.savefig(filename)
    plt.close()
    
