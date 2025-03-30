import os
import subprocess

def extract_frames(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".mp4"):
            input_path = os.path.join(input_folder, file)
            video_name = os.path.splitext(file)[0]
            output_dir = os.path.join(output_folder, video_name)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_pattern = os.path.join(output_dir, "frame_%d.png")

            command = ["ffmpeg", "-i", input_path, output_pattern]

            print(f"Extracting frames from: {file}")
            subprocess.run(command, check=True)
            print(f"Frames saved in: {output_dir}\n")

input_folder = "" 
output_folder = ""
extract_frames(input_folder, output_folder)