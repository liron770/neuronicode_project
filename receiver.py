import os
import time
import subprocess
import cv2
import numpy as np

sdp_path = "stream.sdp"

while not os.path.exists(sdp_path):
    print("[-] Waiting for stream.sdp to be created by sender...")
    time.sleep(1)

print("[+] Found stream.sdp, starting FFmpeg subprocess (whitelisted protocols)...")

ffmpeg_cmd = [
    "ffmpeg",
    "-protocol_whitelist", "file,udp,rtp",
    "-i", sdp_path,
    "-pix_fmt", "bgr24",
    "-s", "1280x720",
    "-f", "rawvideo",
    "-"
]

process = None
try:
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("[+] FFmpeg started")

    width, height = 1280, 720
    frame_size = width * height * 3

    while True:
        raw = process.stdout.read(frame_size)
        if len(raw) < frame_size:
            time.sleep(0.01)
            continue

        frame = np.frombuffer(raw, dtype=np.uint8).reshape((height, width, 3))
        cv2.imshow("RTP Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("[!] Interrupted by user")
except Exception as e:
    print(f"[-] Error while running FFmpeg subprocess: {e}")
finally:
    print("[*] Cleaning up...")
    if process is not None:
        try:
            process.terminate()
            process.wait(timeout=2)
        except Exception:
            pass
    cv2.destroyAllWindows()
    print("[+] Receiver stopped.")
