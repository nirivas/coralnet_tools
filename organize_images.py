import os
import shutil
import argparse

# Function to organize images into folders based on unique identifier
def organize_images(image_folder, destination_base):
    # Ensure destination folder exists
    if not os.path.exists(destination_base):
        os.makedirs(destination_base)

    # Loop through all files in the image folder
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust extensions as necessary
            # Split the filename to extract the unique combination (assumes format: coral_image_Maguey_#_#_###)
            parts = filename.split('_')
            if len(parts) >= 3:
                first_part = parts[0]
                second_part = parts[1]
                unique_id = f'{first_part}-{second_part}-2021'
                
                # Define the destination folder for this unique identifier
                destination_folder = os.path.join(destination_base, unique_id)
                
                # Create the folder if it doesn't exist
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                
                # Move the image to the corresponding folder
                source_path = os.path.join(image_folder, filename)
                destination_path = os.path.join(destination_folder, filename)
                shutil.move(source_path, destination_path)
                
                print(f'Moved: {filename} to {destination_folder}')

# Main function to parse arguments and call the organize function
def main():
    parser = argparse.ArgumentParser(description="Organize images by unique identifiers in their filenames.")
    parser.add_argument('image_folder', help="Path to the folder containing images.")
    parser.add_argument('destination_base', help="Path to the destination folder where images will be organized.")
    
    args = parser.parse_args()
    
    organize_images(args.image_folder, args.destination_base)

if __name__ == "__main__":
    main()
