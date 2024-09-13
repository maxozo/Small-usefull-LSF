#!/usr/bin/env python
import scanpy as sc
import argparse
import os 
def simple_investigation(h5ad_path, var_name):
    # Check if the file exists
    if not os.path.isfile(h5ad_path):
        raise FileNotFoundError(f"The file {h5ad_path} does not exist or is not accessible.")
    
    try:
        # Load the AnnData object
        adata = sc.read_h5ad(filename=h5ad_path)
    except Exception as e:
        raise ValueError(f"Error reading the file: {e}")
    
    # Check if the specified variable exists in adata.var columns
    if var_name in adata.var.columns:
        # Reset the index to add the current index as a column
        adata.var.reset_index(inplace=True)
        
        # Change the index of adata.var to the specified variable
        adata.var.set_index(var_name, inplace=True)
    else:
        raise ValueError(f"Column '{var_name}' not found in adata.var")
    
    # Construct the new file name with the variable name as suffix in the current working directory
    basename = os.path.basename(h5ad_path)
    new_file_name = basename.replace(".h5ad", f"_{var_name}.h5ad")
    new_file_path = os.path.join(os.getcwd(), new_file_name)
    
    # Save the AnnData object to the new file
    try:
        adata.write(new_file_path, compression='gzip')
        print('Done changing index. Saved to:', new_file_path)
    except Exception as e:
        raise ValueError(f"Error saving the file: {e}")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an h5ad file and change var index to a specified gene symbol.')
    parser.add_argument('h5ad_path', type=str, help='Path to the input h5ad file')
    parser.add_argument('var_name', type=str, help='Variable name to set as index in adata.var')
    args = parser.parse_args()
    simple_investigation(args.h5ad_path, args.var_name)