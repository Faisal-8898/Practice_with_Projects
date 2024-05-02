import cv2

# Parameters
input_video_path = './input/glam.mov'
output_video_path = './output/hello.mp4'
slow_motion_factor = 8  # Increase frames by this factor
original_fps = 30  # Original FPS
target_fps = 120  # Target FPS
start_slow_time = 1.9  # Start of slow motion in seconds
end_slow_time = 6.1   # End of slow motion in seconds
zoom_peak = 1.4  # Peak zoom factor (130%)

# Open the video
cap = cv2.VideoCapture(input_video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Setup output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, target_fps, (width, height))

# Read frames and process
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()

# Processing frames for slow motion and zoom
total_slow_duration = end_slow_time - start_slow_time
slow_frames_count = total_slow_duration * original_fps
half_slow_frames = slow_frames_count / 2

for i, frame in enumerate(frames):
    current_time = i / original_fps  # Current time in seconds

    # Apply slow motion with zoom effect
    if start_slow_time <= current_time <= end_slow_time:
        zoom_factor = 1 + (zoom_peak - 1) * (abs(i - slow_frames_count/2) / (slow_frames_count/2))
        zoomed_frame = cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_LINEAR)
        x_center = zoomed_frame.shape[1] // 2
        y_center = zoomed_frame.shape[0] // 2
        zoomed_frame = zoomed_frame[y_center-height//2:y_center+height//2, x_center-width//2:x_center+width//2]
        out.write(zoomed_frame)
        for j in range(1, slow_motion_factor):
            next_frame = frames[i + 1] if i + 1 < len(frames) else frame
            alpha = j / slow_motion_factor
            frame_interpolated = cv2.addWeighted(frame, 1 - alpha, next_frame, alpha, 0)
            zoomed_interpolated = cv2.resize(frame_interpolated, None, fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_LINEAR)
            zoomed_interpolated = zoomed_interpolated[y_center-height//2:y_center+height//2, x_center-width//2:x_center+width//2]
            out.write(zoomed_interpolated)
    else:
        out.write(frame)

out.release()
print('Video processing complete.')