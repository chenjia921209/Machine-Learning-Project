import pandas as pd
import glob

def merge_csv_files(pattern="*.csv", output="merged_food_data.csv"):
    # \find all files matching the pattern
    files = glob.glob(pattern)
    print("Found files:", files)

    # read and merge all CSV files
    dfs = [pd.read_csv(f) for f in files]
    # use .concat to merge dataframes
    merged = pd.concat(dfs, ignore_index=True)

    # delete duplicate rows
    merged = merged.drop_duplicates()

    # save the merged dataframe to a new CSV file
    merged.to_csv(output, index=False)

if __name__ == "__main__":
    merge_csv_files(pattern="FOOD-DATA-GROUP*.csv")