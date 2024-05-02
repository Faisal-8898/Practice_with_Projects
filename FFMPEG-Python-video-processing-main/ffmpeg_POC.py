# Step 1: FFmpeg Wrapper Function
def run_ffmpeg_command(command):
    import subprocess
    import os

    if os.path.exists(output_path):
        os.remove(output_path)
    
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout, process.stderr

# Step 2: Get Video Duration
def get_video_duration(video_path):
    command = f"ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {video_path}"
    output, _ = run_ffmpeg_command(command)
    return float(output.strip())

# Step 3: Apply Effects and Merge Videos with Consistent Frame Rate and Transitions
def apply_effects_and_merge(videos, output_path):
    durations = [get_video_duration(video) for video in videos]
    filter_complex_parts = []

    # Setup input videos with consistent frame rate and format
    for i, video in enumerate(videos):
        filter_complex_parts.append(f"[{i}:v] fps=fps=30, format=yuva420p [v{i}]")
        
    # jump_duration = 0.2
    # overlay_start_time = 2
    # temp_time = overlay_start_time + jump_duration
    # overlay_end_time = []
    
    # for i in range(0, 5):
    #     temp_time += jump_duration
    #     overlay_end_time.append(temp_time)

    # second_effect_time = overlay_end_time[4]

    filter_complex_parts.append(f"[0:v] fps=fps=30 [vfps1]")
    filter_complex_parts.append(f"[vfps1][v0] xfade=transition=fadewhite:duration={1}:offset={1.7} [vfade0]")
    
    # Use the enable='between(t,START_TIME,END_TIME)' option to apply the overlay effect only for the specified duration
    filter_complex_parts.append(f"[vfade0][v1] overlay=shortest=1:enable='between(t,{overlay_start_time},{overlay_end_time[0]})' [v01]")
    filter_complex_parts.append(f"[v01][v2] overlay=shortest=1:enable='between(t,{overlay_end_time[0]},{overlay_end_time[1]})' [v02]")
    filter_complex_parts.append(f"[v02][0:v] overlay=shortest=1:enable='between(t,{overlay_end_time[1]},{overlay_end_time[2]})' [v03]")
    filter_complex_parts.append(f"[v03][1:v] overlay=shortest=1:enable='between(t,{overlay_end_time[2]},{overlay_end_time[3]})' [v04]")
    filter_complex_parts.append(f"[v04][2:v] overlay=shortest=1:enable='between(t,{overlay_end_time[3]},{overlay_end_time[4]})' [v05]")
    
    # filter_complex_parts.append(f"[v05][0:v] concat=n=2:v=1:a=0 [v]")

    filter_complex_parts.append(f"[0:v] setpts=PTS, scale=340x620 [upperleft]")
    filter_complex_parts.append(f"[1:v] setpts=PTS, scale=340x620 [upperright]")
    filter_complex_parts.append(f"[2:v] setpts=PTS, scale=360x620 [bottom]")

    filter_complex_parts.append(f"[v05][upperleft] overlay=shortest=1:x=10:y=10:enable='between(t,{second_effect_time},{second_effect_time + 4})' [v06]")
    filter_complex_parts.append(f"[v06][upperright] overlay=shortest=1:x=370:y=10:enable='between(t,{second_effect_time},{second_effect_time + 4})' [v07]")
    filter_complex_parts.append(f"[v07][bottom] overlay=shortest=1:x=180:y=650:enable='between(t,{second_effect_time},{second_effect_time + 4})' [v08]")
    
    filter_complex_parts.append(f"[v08] fps=fps=30 [v08fps]")
    filter_complex_parts.append(f"[0:v] fps=fps=30 [vfps]")
    
    filter_complex_parts.append(f"[v08fps][vfps] xfade=transition=fade:duration={4}:offset={second_effect_time} [vfade1]")

    filter_complex_parts.append(f"[vfade1] trim={0}:{7} [vfade1trimmed]")

    # Punch zoom effect on vfade1 just before transitioning to [1:v]
    punch_zoom_start = durations[0] - 4  # 4 seconds before the first video ends, adjust as needed
    filter_complex_parts.append(f"[0:v] trim=start={7}:end={8}:duration=1,setpts=PTS-STARTPTS,zoompan=z='if(lte(zoom,4.5),1.2*zoom,4.5)':d=30:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)', scale=720:1280, setsar=1 [zoomed]")
    filter_complex_parts.append(f"[zoomed] trim=start={0}:end={0.2},setpts=PTS-STARTPTS [zoomedtrimmed]")
    filter_complex_parts.append(f"[1:v] trim=start={0}:end={3},setpts=PTS-STARTPTS [endv]")
    filter_complex_parts.append(f"[vfade1trimmed][zoomedtrimmed][endv] concat=n=3:v=1:a=0 [final]")
    # filter_complex_parts.append(f"[punched][1:v] overlay=shortest=1:enable='between(t,{punch_zoom_start},{durations[0]})' [v09]")

    # Join the filter parts correctly
    filter_complex_string = ';'.join(filter_complex_parts)
    inputs = " ".join([f"-i {video}" for video in videos])
    command = f"ffmpeg {inputs} -filter_complex \"{filter_complex_string}\" -r 30 -map [final] {output_path}"

    print("Executing command:", command)
    _, error = run_ffmpeg_command(command)
    if error:
        print("Error applying effects and merging videos:", error)


# Define input videos and output path
videos = ["input/input_1.mp4", "input/input_2.mp4", "input/input_3.mp4"]
output_path = "output/output_video.mp4"

# Uncomment the line below to apply effects and merge the videos when running in a suitable environment
apply_effects_and_merge(videos, output_path)
