from analyzers import Analysis
from writers import Writer
from utils.thread_manager import ThreadManager
from utils.checkpointer import Checkpointer
from datasets import Dataset

class Processor:
    def __init__(
        self,
        analyzer: Analysis,
        writer: Writer,
        batch_size: int = 100,
        checkpointer: Checkpointer = None
    ):
        self.__threader = ThreadManager(analyzer)
        self.__writer = writer
        self.__batch_size = batch_size
        self.__checkpointer = checkpointer
    
    def process_data(
        self,
        dataset: Dataset
    ):
        batch_num = 1
        while len(dataset) != 0:
            # Load the current batch
            current_batch = []
            while len(current_batch) < self.__batch_size and len(dataset) != 0:
                current_batch.append(dataset.pop())
            
            # Submit batch
            batch_results = self.__threader.submit_batch(current_batch)

            # Write the results to the file.
            self.__writer.write_batch(batch_results)

            if self.__checkpointer:
                if not self.__checkpointer.interval % batch_num:
                    self.__checkpointer.checkpoint()
                
            batch_num += 1

