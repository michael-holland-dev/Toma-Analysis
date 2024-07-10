from analyzers import Analysis
import threading


class ThreadManager:
    def __init__(
        self,
        analyzer: Analysis
    ):
        self.analyzer = analyzer
    
    def submit_batch(
        self,
        batch: list
    ):
        results = []
        threads = []
        for datapoint in batch:
            if type(datapoint) != dict:
                raise Exception("Datapoint Must be in Dictionary Format")
            
            datapoint: dict = datapoint
            thread = threading.Thread(target=self.analyzer.analyze, kwargs=datapoint.update({"results": results}))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return results
