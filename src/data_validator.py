import pandas as pd

class Validation:
    def __init__(self, file1_path, file2_path, min_rows=100, max_rows=10000):
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.min_rows = min_rows
        self.max_rows = max_rows

    def validate_files(self):
        try:
            data1 = pd.read_csv(self.file1_path)
            data2 = pd.read_csv(self.file2_path)
        except Exception as e:
            return f"Error reading files: {e}"

        valid1, msg1 = self.validate_data(data1)
        valid2, msg2 = self.validate_data(data2)

        if not valid1:
            return f"File 1 validation failed: {msg1}"
        if not valid2:
            return f"File 2 validation failed: {msg2}"

        return "Both files are successfully validated."

    def validate_data(self, data):
        if len(data.columns) != 2:
            return False, "File must contain exactly two columns."

        if not all(pd.api.types.is_numeric_dtype(data[col]) for col in data.columns):
            return False, "All data (excluding headers) must be numeric."

        if len(data) < self.min_rows or len(data) > self.max_rows:
            return False, f"File length must be between {self.min_rows} and {self.max_rows} rows."

        if not all(data.iloc[:, 0] == sorted(data.iloc[:, 0])):
            return False, "Data must be sorted ascending by the timestep column."

        if len(data.iloc[:, 0]) != len(data.iloc[:, 1]):
            return False, "Both columns must be of the same length."

        return True, "Data is valid."

# Example usage:
#validator = Validation('DataFile1.csv', 'DataFile2.csv', 10, 100)
#print(validator.validate_files())
