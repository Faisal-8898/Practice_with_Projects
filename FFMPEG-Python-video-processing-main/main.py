import os
import subprocess

# Step 1: FFmpeg Wrapper Function
def run_ffmpeg_command(command):
    # Ensure the output directory is clear before running the command
    if os.path.exists(output_path):
        os.remove(output_path)

    # Execute the FFmpeg command and capture output
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout, process.stderr

# Step 2: Get Video Duration
def get_video_duration(video_path):
    command = f"ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {video_path}"
    output, _ = run_ffmpeg_command(command)
    return float(output.strip())

# Step 3: Apply Effects and Merge Videos with Specific Effects at Checkpoints
def apply_effects(video_path, output_path):
    duration = get_video_duration(video_path)
    checkpoints = [duration / 3, 2 * duration / 3, duration]  # Three equal checkpoints

    # Building the filter complex command
    filter_complex_parts = []
    
    filter_complex_parts.append(f"[0:v] fps=fps=30, format=yuv420p [base0]")  # Initial format and fps setup
    filter_complex_parts.append(f"[0:v] fps=fps=30, format=yuv420p [base1]")  # Initial format and fps setup
    filter_complex_parts.append(f"[0:v] fps=fps=30, format=yuv420p [base2]")  # Initial format and fps setup
    
    filter_complex_parts.append(f"[base0] trim=0:{checkpoints[0]}, setpts=PTS-STARTPTS [first_part]")  # First part, normal speed
    filter_complex_parts.append(f"[base1] trim={checkpoints[0]}:{checkpoints[1]}, setpts=3*(PTS-STARTPTS) [second_part]")  # Second part, increased fps
    filter_complex_parts.append(f"[base2] trim={checkpoints[2]}:{checkpoints[0]*3+duration}, setpts=3*(PTS-STARTPTS), zoompan=z='min(zoom+0.2,5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)', scale={width}:{height}, setsar=1 [third_part]")  # Third part, zoom effect
    
    
    # Here we need to fix
    filter_complex_parts.append(f"[second_part] minterpolate='fps=120:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:me=umh:mb_size=16:search_param=4:vsbmc=1:scd=fdiff:scd_threshold=5' [a]")
    filter_complex_parts.append(f"[third_part] minterpolate='fps=120:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:me=umh:mb_size=16:search_param=4:vsbmc=1:scd=fdiff:scd_threshold=5' [b]")

    
    filter_complex_parts.append(f"[first_part][a][b] concat=n=3:v=1:a=0 [output]")  # Concatenate all parts

    # Combine all filter parts into a single filter_complex string
    filter_complex_string = ";".join(filter_complex_parts)
    command = f"ffmpeg -i {video_path} -filter_complex \"{filter_complex_string}\" -map [output] {output_path}"

    print("Executing command:", command)
    _, error = run_ffmpeg_command(command)
    if error:
        print("Error applying effects:", error)

# Define input video and output path
video_path = "input/i3.mp4"
output_path = "output/output_video_3.mp4"

command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0:s=x',  # Output format is widthxheight
        video_path
    ]

process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
if process.returncode == 0:
        output = process.stdout.strip()
        width, height = map(int, output.split('x'))

apply_effects(video_path, output_path)
