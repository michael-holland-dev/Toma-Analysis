from .file_writer import FileWriter  # Import FileWriter class from file_writer module
import csv                          # Import csv module for CSV file operations

class CSVWriter(FileWriter):
    """
    A class to write data to a CSV file, inheriting from FileWriter.

    Attributes:
    - filename (str): Name of the CSV file to write.
    - fieldnames (list): List of field names for the CSV header.
    - file (file object): File object representing the open CSV file.
    - writer (csv.writer object): CSV writer object for writing rows.
    """

    def __init__(self, filename, fieldnames):
        """
        Initialize CSVWriter with filename and fieldnames.

        Args:
        - filename (str): Name of the CSV file to write.
        - fieldnames (list): List of field names for the CSV header.
        """
        self.filename = filename  # Set the filename attribute
        self.fieldnames = fieldnames  # Set the fieldnames attribute
        self.file = open(filename, 'w', newline='', encoding='utf-8')  # Open CSV file for writing
        self.writer = csv.writer(self.file)  # Create CSV writer object
        self.writer.writerow(self.fieldnames)  # Write header row

    def write_open(self):
        """
        Reopen CSV file in append mode for writing additional rows.
        """
        self.file = open(self.filename, 'a', newline='', encoding='utf-8')  # Reopen CSV file in append mode
        self.writer = csv.writer(self.file)  # Create CSV writer object

    def write_row(self, row):
        """
        Write a single row of data to the CSV file.

        Args:
        - row (list): List representing a row of data to write.
        """
        self.writer.writerow(row)  # Write the provided row to the CSV file

    def write_rows(self, dict):
        """
        Write multiple rows of data to the CSV file.

        Args:
        - dict (dict): Dictionary where keys are row identifiers and values are lists representing rows of data.
        """
        for key in dict:
            self.writer.writerow(dict[key])  # Write each row from the dictionary to the CSV file
            self.file.flush()  # Flush the buffer to ensure data is written immediately

    def close(self):
        """
        Close the CSV file.
        """
        self.file.close()  # Close the CSV file


#if __name__ == "__main__":