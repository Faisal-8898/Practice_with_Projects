import cv2
import os

# Function to delete a file
def delete_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

# Load the video
video_path = 'input/glam.mov'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Unable to open video file")
    exit()

# Get the frame width and height of the original video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Get the frame rate of the original video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

# Determine the frame ranges for each part
part1_end_frame = int(0.75 * fps)
part2_end_frame = int(1.2 * fps)

# Create temporary video files for each part
temp_dir = 'temp/'
os.makedirs(temp_dir, exist_ok=True)

part1_path = os.path.join(temp_dir, 'part1.mp4')
part2_path = os.path.join(temp_dir, 'part2.mp4')
part3_path = os.path.join(temp_dir, 'part3.mp4')

# VideoWriter parameters for output parts
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_params = (fourcc, fps, (width, height))

# Create VideoWriter objects for each part
part1_out = cv2.VideoWriter(part1_path, fourcc, fps, (width, height))
part2_out = cv2.VideoWriter(part2_path, fourcc, fps, (width, height))
part3_out = cv2.VideoWriter(part3_path, fourcc, fps, (width, height))

# Read and write frames for each part
frame_number = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Write frame to the appropriate part
    if frame_number < part1_end_frame:
        part1_out.write(frame)
    elif part1_end_frame <= frame_number < part2_end_frame:
        part2_out.write(frame)
    else:
        part3_out.write(frame)
    
    frame_number += 1

# Release resources for input video
cap.release()

# Release resources for each part's VideoWriter
part1_out.release()
part2_out.release()
part3_out.release()

# Now, apply slow-motion to the middle part (part2)
part2_slow_path = os.path.join(temp_dir, 'part2_slow.mp4')
part2_slow_out = cv2.VideoWriter(part2_slow_path, fourcc, fps / 4, (width, height))

cap_part2 = cv2.VideoCapture(part2_path)
frame_number = 0
while cap_part2.isOpened():
    ret, frame = cap_part2.read()
    if not ret:
        break

    # Write each frame 16 times to slow down the video
    for _ in range(4):
        part2_slow_out.write(frame)
    
    frame_number += 1

# Release resources for part2 input video
cap_part2.release()
part2_slow_out.release()

# Now, concatenate the three parts (normal, slow-motion, normal)
output_path = 'output/concatenated_video.mp4'
os.system(f'ffmpeg -i {part1_path} -i {part2_slow_path} -i {part3_path} -filter_complex "[0:v] [1:v] [2:v] concat=n=3:v=1 [v]" -map "[v]" {output_path}')

# Delete temporary video files
# delete_file(part1_path)
# delete_file(part2_path)
# delete_file(part2_slow_path)
# delete_file(part3_path)

# Cleanup temp directory
# os.rmdir(temp_dir)

# Inform user
print("Concatenated video generated successfully!")
