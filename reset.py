import os
import shutil

source_directories = ["media", "images", "executables", "other"]
destination_directory = "testingdir"

for source_dir in source_directories:
    for root, _, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_directory, file)
            shutil.move(source_path, destination_path)

print("Files moved successfully.")
