import os
import subprocess

TASK_KILL_FFMPEG = "taskkill /f /im ffmpeg.exe"
TASK_KILL_PYTHON = "taskkill /f /im python.exe"
SDP_FILE = "stream.sdp"
METRICS_FILE = "metrics.json"

SUBPROCESS_CONFIG = {
    "stdout": subprocess.PIPE,
    "stderr": subprocess.DEVNULL,
    "text": True,
}

COMMANDS = {
    "sender": ["python", "sender.py","videoRoadTraffic.mp4"], 
    "receiver": ["python", "receiver.py","videoRoadTraffic.mp4"]}
