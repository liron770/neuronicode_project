import subprocess

TASK_KILL_FFMPEG = "taskkill /f /im ffmpeg.exe"
SDP_FILE = "stream.sdp"
METRICS_FILE = "metrics.json"

SUBPROCESS_CONFIG = {
    "stdout": subprocess.PIPE,
    "stderr": subprocess.DEVNULL,
    "text": True,
}

COMMANDS = {"sender": ["python", "sender.py"], "receiver": ["python", "receiver.py"]}
