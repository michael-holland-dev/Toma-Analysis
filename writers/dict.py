from writers import Writer
import pandas as pd
import os
import json


class DICT(Writer):
    def __init__(self, output_file="./myfile.csv"):
        self.file_path = output_file
        self.data = {}
        self._load_existing_data()

    def _load_existing_data(self):
        """
        Load existing data from the JSON file if it exists.
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as json_file:
                    self.data = json.load(json_file)
                print(f"Data loaded from {self.file_path}.")
            except json.JSONDecodeError:
                print(f"The file {self.file_path} is empty or contains invalid JSON. Starting with an empty dictionary.")
                self.data = {}
        else:
            print(f"No existing file found. A new file will be created at {self.file_path}.")
            self.data = {}
    def write(self, results: dict, **kwargs):
        try:
            # Read the existing data from the file
            try:
                with open(self.file_path, 'r') as json_file:
                    data = json.load(json_file)
            except FileNotFoundError:
                data = {}  # Start with an empty dictionary if the file doesn't exist

            # Update the existing data with the new data
            data.update(results)

            # Write the updated data back to the file
            with open(self.file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            print(f"Data appended to {self.file_path} successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
         
    def finish_and_save(self):
        """
        Save the accumulated DataFrame to the CSV file.
        """
        self.df.to_csv(self.file_path, index=False)
        print(f"Data saved to {self.file_path}")
