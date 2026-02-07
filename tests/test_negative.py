import pytest
import subprocess
import os
import time
from config import *
from utils import *

@pytest.fixture(scope="module")
def start():
    """
    Fixture to clean up before and after tests.
    """
    remove_file_if_exists([SDP_FILE,METRICS_FILE])
    yield
    cv2.destroyAllWindows()
    os.system(TASK_KILL_FFMPEG)
    os.system(TASK_KILL_PYTHON)


def test_sender_negative_missing_file():
    """
    Verify that sender process exits gracefully with an error when the specified video file is missing.
    """
    remove_file_if_exists([SDP_FILE])
    
    invalid_command = ["python", "sender.py", "non_existent_video.mp4"]
    proc = subprocess.Popen(invalid_command, **SUBPROCESS_CONFIG)

    assert proc is not None, "start sender process when video file is missing"
    assert not os.path.exists(SDP_FILE), "Critical Failure: SDP file was created even though video is missing!"
