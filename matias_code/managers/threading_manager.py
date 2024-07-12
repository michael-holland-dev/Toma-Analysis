import threading
from queue import Queue

def thread(batch: list, task: callable, num_threads: int = 6) -> dict:
    results_queue = Queue()
    threads = []
    
    # Create and start the specified number of threads
    for tomo_link in batch:
        thread = threading.Thread(target=task, args=(tomo_link, results_queue))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Collect results from the queue
    results = {}
    while not results_queue.empty():
        file, result = results_queue.get()
        results[file] = result

    return results
