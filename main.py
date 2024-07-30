import os
import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import subprocess
import platform

def load_csv_data(file_path=None):
    if file_path is None:
        # Setup the root tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Open a file dialog to select the CSV file
        file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])

    # Load the data from the provided file path
    if file_path:
        data = pd.read_csv(file_path)
        
        # Print a preview of the data (first 5 rows)
        print("Data preview:")
        print(data.head())
        
        # Print completion message
        print("Data load complete!")
        return data, file_path
    else:
        print("No file was provided.")
        return None, None

def generate_api_endpoints(df):
    if df is not None:
        print("Generating API endpoints...")
        # Filter out rows where 'file_source_id' is null
        df = df[df['file_source_id'].notna()]

        # Generate the 'api_endpoint' column
        df['api_endpoint'] = df.apply(lambda row: f"https://intelligence-platform-api-internal.app.janus-ai.com/private-api/observe/v1/{row['org_id']}/file/{row['file_source_id']}?fileName={row['path']}", axis=1)

        # Print a preview of the data
        print("Data preview with API endpoints:")
        print(df.head())

        # Print completion message
        print("API endpoints generated")
        return df
    else:
        print("No data to process")
        return None

def create_directory_and_download_images(df, file_path):
    if df is not None:
        print("Creating directory and downloading images...")
        # Extract directory and file base from file_path
        directory, file_name = os.path.split(file_path)
        base_name = os.path.splitext(file_name)[0]
        images_dir = os.path.join(directory, f"{base_name}_images")

        # Create directory if it does not exist
        os.makedirs(images_dir, exist_ok=True)

        # Download and save images
        for index, row in df.iterrows():
            image_url = row['api_endpoint']
            event_number = row['event_number']
            file_name = f"{int(event_number):05d}.jpg"
            image_path = os.path.join(images_dir, file_name)

            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
        
        # Completion message
        print("Images downloaded")
        return images_dir
    return None

def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # Linux
        subprocess.Popen(["xdg-open", path])

# Execute the functions
if __name__ == "__main__":
    file_path = input("Please enter the path to the CSV file: ")
    data, file_path = load_csv_data(file_path)
    if data is not None:
        data = generate_api_endpoints(data)
        images_dir = create_directory_and_download_images(data, file_path)
        if images_dir:
            open_folder(images_dir)
    print("Script execution completed.")
