import os
import json
import shutil
from pathlib import Path

# Configuration
POSSIBLE_FLAGS = {"black_image", "not_inundated", "inundated", "laantjes"}
SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp"]

def find_image_file(json_path):
    """Find the image file that has the same stem name as the JSON."""
    json_stem = json_path.stem
    folder = json_path.parent
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        image_path = folder / f"{json_stem}{ext}"
        if image_path.exists():
            return image_path
    return None

def process_labelme_folder(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Folder does not exist: {folder}")
        return

    json_files = list(folder.glob("*.json"))

    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        flags = data.get("flags", {})
        if not flags:
            continue  # Skip if no flags

        for flag, value in flags.items():
            if value and flag in POSSIBLE_FLAGS:
                subfolder = folder / flag
                subfolder.mkdir(exist_ok=True)

                image_file = find_image_file(json_file)
                if not image_file:
                    print(f"Warning: Image file not found for {json_file}")
                    continue

                # Move both JSON and image to subfolder
                shutil.move(str(json_file), subfolder / json_file.name)
                shutil.move(str(image_file), subfolder / image_file.name)
                print(f"Moved {json_file.name} and {image_file.name} to {subfolder}")
                break  # Avoid moving the same file multiple times if multiple flags are True

if __name__ == "__main__":
    #path = "G:/Gedeelde drives/Team_BioDiv/5_Projecten/2024_Biodiversa_habitatpilot/WP2_3/Inundation/Segmentation_orthos/Cropped_orthos_tiles/Kloosterbeemden/2020"
    path = "G:/Gedeelde drives/Team_BioDiv/5_Projecten/2024_Biodiversa_habitatpilot/WP2_3/Inundation/Segmentation_orthos/Cropped_orthos_tiles/Kloosterbeemden/2021"
    process_labelme_folder(path)