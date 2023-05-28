import pandas as pd

# List of file paths
file_paths = ['/home/cev/project/brake/output.csv', '/home/cev/project/handle/turn_speed.csv', '/home/cev/project/ultrasound/2023-05-01_08-02-09.csv']

# Read the first file to create the initial DataFrame
merged_data = pd.read_csv(file_paths[0])

# Loop through the remaining files and merge them by column
for file_path in file_paths[1:]:
    data = pd.read_csv(file_path)
    merged_data = pd.concat([merged_data, data], axis=1)

# Write the merged data to a new CSV file
merged_data.to_csv('merged.csv', index=False)
