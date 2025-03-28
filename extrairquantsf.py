import os
import pandas as pd

def extract_fourth_column(main_folder):
    data = {}
    
    # Loop through each subfolder in the main folder
    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)
        
        # Check if it's a directory
        if os.path.isdir(subfolder_path):
            quant_file = os.path.join(subfolder_path, "quant.sf")
            
            # Check if the quant.sf file exists
            if os.path.exists(quant_file):
                try:
                    # Read the file and extract the fourth column
                    df = pd.read_csv(quant_file, sep="\t", header=0, engine='python')
                    
                    # Extract the fourth column
                    fourth_column = df.iloc[:, 3].values.tolist()
                    
                    # Insert the folder name as the first element
                    fourth_column.insert(0, subfolder)
                    
                    # Store the column data
                    data[subfolder] = fourth_column
                except Exception as e:
                    print(f"Erro ao ler {quant_file}: {e}")

    # Create a DataFrame from the collected data
    result_df = pd.DataFrame.from_dict(data, orient='columns')
    
    # Save to a new file in the current directory
    output_file = os.path.join(os.getcwd(), "merged_quant_data.csv")
    result_df.to_csv(output_file, index=False, header=True)
    print(f"Arquivo salvo em: {output_file}")

# Replace 'main_folder_path' with the actual path to the main directory
main_folder_path = "\home\lucas\truncatussalmon\salmon"
extract_fourth_column(main_folder_path)
