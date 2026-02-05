import subprocess
import time
import os

def start_sender():
    video_source = "videoRoadTraffic.mp4"  
    sdp_path = "stream.sdp"

    if not os.path.exists(video_source):
        print(f"[-] Error: {video_source} not found!")
        return

    ffmpeg_cmd = [
        'ffmpeg',
        '-re',                         
        '-stream_loop', '-1',          
        '-i', video_source,
        '-vf', 'scale=1280:720',       
        '-r', '25',                    
        '-c:v', 'libx264',            
        '-preset', 'ultrafast',         
        '-tune', 'zerolatency',       
        '-f', 'rtp',
        '-sdp_file', sdp_path,         
        'rtp://127.0.0.1:5004'
    ]

    print("[+] Starting FFmpeg RTP H.264 stream...")
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Stopping sender...")
    finally:
        if ffmpeg_process.poll() is None:
            ffmpeg_process.terminate()
        print("[+] Sender stopped.")

if __name__ == "__main__":
    start_sender()