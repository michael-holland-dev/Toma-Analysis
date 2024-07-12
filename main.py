from writers import CSVWriter
from managers import task_batcher, thread
from analyzers import numpy_analysis

###-------------- Main variables --------------###

# Define output file
csv_output_file = 'test.csv'

# Header
header = ["Directory", "Bacteria", "Name", "Data Shape", "Mean", "Min value", "Max value", "SIRT"]

# number of random samples to analyze in the database
sample = True
n_sample = 25
batch_size = 4


#root_search_path = "/Users/matiasgomezpaz/Documents/RESEARCH" 
root_search_path = ["/home/matiasgp/groups/grp_tomo_db1_d1/nobackup/archive/TomoDB1_d1/FlagellarMotor_P1", 
                    "/home/matiasgp/groups/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2", 
                    "/home/matiasgp/groups/grp_tomo_db1_d3/nobackup/archive/TomoDB1_d3", 
                    "/home/matiasgp/groups/grp_tomo_db1_d4/nobackup/archive/TomoDB1_d4"]

# Start processing
task_batcher(
    root_paths=root_search_path,
    batch_size=batch_size,
    thread=thread,
    analyzer_task=numpy_analysis,
    writer=CSVWriter(csv_output_file, header),
    sample=sample,
    sample_size=n_sample
)