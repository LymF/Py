import pandas as pd
import argparse

def read_file(file, col):
    if file.endswith(".xlsx"):
        df = pd.read_excel(file, usecols=[col], dtype=str)
    elif file.endswith(".csv"):
        df = pd.read_csv(file, usecols=[col], dtype=str)
    elif file.endswith(".tsv"):
        df = pd.read_csv(file, usecols=[col], dtype=str, sep='\t')
    else:
        raise ValueError("Unsupported file format. Please use CSV, TSV, or XLSX.")
    return set(df.iloc[:, 0].dropna())

def compare_files(file1, file2, col1, col2):
    set1 = read_file(file1, col1)
    set2 = read_file(file2, col2)
    
    missing_in_file2 = set1 - set2
    missing_in_file1 = set2 - set1
    
    if missing_in_file2:
        print("Present in", file1, "but missing in", file2, ":")
        for item in missing_in_file2:
            print(item)
    else:
        print("No missing entries in", file2)
    
    if missing_in_file1:
        print("Present in", file2, "but missing in", file1, ":")
        for item in missing_in_file1:
            print(item)
    else:
        print("No missing entries in", file1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two CSV, TSV, or XLSX files based on specified columns.")
    parser.add_argument("-file1", type=str, required=True, help="Path to the first file (CSV, TSV, or XLSX)")
    parser.add_argument("-file2", type=str, required=True, help="Path to the second file (CSV, TSV, or XLSX)")
    parser.add_argument("-col1", type=int, required=True, help="Column number to be checked in the first file (zero-indexed)")
    parser.add_argument("-col2", type=int, required=True, help="Column number to be checked in the second file (zero-indexed)")
    
    args = parser.parse_args()
    compare_files(args.file1, args.file2, args.col1, args.col2)
