from writers.writer_base import Writer
from writers.csv import CSV
from writers.excel import Excel

def get_writer(
        writer_string: str = "csv",
        output_folder: str = None
    ):
    writer_string = writer_string.lower()
    
    if writer_string == "csv":
        return CSV
    elif writer_string == "xlsx":
        return Excel
    else:
        raise Exception("Writer does not exist")