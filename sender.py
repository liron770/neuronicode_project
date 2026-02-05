import subprocess
import time
import signal

video_source = "videoRoadTraffic.mp4"  
sdp_path = "stream.sdp"

ffmpeg_cmd = [
    "ffmpeg",
    "-re",                       
    "-stream_loop", "-1",       
    "-i", video_source,
    "-vf", "scale=1280:720",
    "-r", "25",
    "-c:v", "libx264",
    "-profile:v", "baseline",
    "-level", "3.1",
    "-pix_fmt", "yuv420p",
    "-g", "25",
    "-keyint_min", "25",
    "-b:v", "2M",
    "-maxrate", "2M",
    "-bufsize", "4M",
    "-x264-params", "repeat-headers=1:nal-hrd=cbr",
    "-an",                     
    "-f", "rtp",
    "-sdp_file", sdp_path,
    "rtp://127.0.0.1:5004"
]

print("[+] Starting FFmpeg RTP stream...")
ffmpeg_process = subprocess.Popen(ffmpeg_cmd)

try:
    while True:
        # מחכה שהסטרים ירוץ
        time.sleep(1)
except KeyboardInterrupt:
    print("[!] Interrupted by user, stopping stream...")
finally:
    if ffmpeg_process.poll() is None:
        ffmpeg_process.send_signal(signal.SIGINT)
        ffmpeg_process.wait()
    print("[+] Sender stopped.")
