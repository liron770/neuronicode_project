import os
import time
import subprocess
import cv2
import numpy as np
import json


def start_receiver():
    sdp_path = "stream.sdp"
    width, height = 1280, 720
    frame_size = width * height * 3

    metrics = {"total_frames": 0, "detected_frames": 0, "latencies": []}

    car_cascade = cv2.CascadeClassifier("cars.xml")
    if car_cascade.empty():
        print("[-] Error: Could not load cars.xml!")
        return

    while not os.path.exists(sdp_path):
        print("[-] Waiting for stream.sdp to be created by sender...")
        time.sleep(1)

    ffmpeg_cmd = [
        "ffmpeg",
        "-protocol_whitelist",
        "file,udp,rtp",
        "-i",
        sdp_path,
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-an",
        "-",
    ]

    process = subprocess.Popen(
        ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    print("[+] Receiver started. Processing stream...")

    try:
        while True:
            start_time = time.time()
            raw = process.stdout.read(frame_size)
            if not raw or len(raw) < frame_size:
                continue
            frame = (
                np.frombuffer(raw, dtype=np.uint8).reshape((height, width, 3)).copy()
            )
            metrics["total_frames"] += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.05, 5, minSize=(50, 50))
            if len(cars) > 0:
                metrics["detected_frames"] += 1
                for x, y, w, h in cars:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            latency = (time.time() - start_time) * 1000
            metrics["latencies"].append(latency)
            report = {
                "total_frames": metrics["total_frames"],
                "detected_frames": metrics["detected_frames"],
                "detection_ratio": round(
                    metrics["detected_frames"] / metrics["total_frames"], 2
                ),
                "avg_latency_ms": round(
                    sum(metrics["latencies"]) / len(metrics["latencies"]), 2
                ),
                "max_latency_ms": (
                    round(max(metrics["latencies"]), 2) if metrics["latencies"] else 0
                ),
            }
            with open("metrics.json", "w") as f:
                json.dump(report, f, indent=4)
            cv2.putText(
                frame,
                f"Frames: {metrics['total_frames']}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
            )
            cv2.imshow("QA Vehicle Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except Exception as e:
        print(f"[-] Runtime Error: {e}")
    finally:
        if process:
            process.terminate()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_receiver()
