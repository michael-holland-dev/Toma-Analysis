from writers import Writer
import matplotlib.pyplot as plt
import os
from utils.graph_plotter import GraphPlotter

class SegmentationSaver(Writer):
    def __init__(self, bacteria_name, output_file="./segmentation_images/"):
        super().__init__(output_file)
        self.bacteria_name = bacteria_name
        self.bacteria_folder = os.path.join(self.file_path, bacteria_name)
        if not os.path.exists(self.bacteria_folder):
            os.makedirs(self.bacteria_folder)
    
    def write(self, results: dict, **kwargs):
        for key, value in results.items():
            fig, axes = plt.subplots(1, 3)

            for ax in axes:
                ax.set_xticks([])
                ax.set_yticks([])


            axes[0].set_title("Original")
            axes[0].imshow(value["image"], cmap="gray")

            axes[1].set_title("Segmentation")
            axes[1].imshow(value["image"], cmap="gray")
            GraphPlotter.show_mask(value["mask"], axes[1])

            axes[2].imshow(value["image"], cmap="gray")
            axes[2].set_title("Seg W/ Points")
            GraphPlotter.show_mask(value["mask"], axes[2])
            GraphPlotter.show_points(value["pts"]["coords"], value["pts"]["labels"], axes[2])

            fig.suptitle(f"{self.bacteria_name} Segmentation Slice Idx: {value['idx']}", y=.8, fontsize=15)
            fig.tight_layout()

            plt.savefig(os.path.join(self.bacteria_folder, f"{self.bacteria_name}_seg_{key}.png"))