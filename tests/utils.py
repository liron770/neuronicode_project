import json
import os
import time
import pytest
import subprocess
import cv2


def cleanup_processes(processes):
    """
    Terminate and clean up a list of subprocesses gracefully.
     :param processes: List of subprocess.Popen objects
    """
    print("---Starting cleanup---")
    for proc in processes:
        if proc and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=3)
                print(f"    - Process {proc.pid} terminated gracefully.")
            except subprocess.TimeoutExpired:
                print(f"    - Process {proc.pid} stuck, killing it...")
                proc.kill()
                proc.wait()
    cv2.destroyAllWindows()
    print("---Cleanup complete. All processes stopped and windows closed.---")


def wait_for_file(file_path, timeout, cleanup_proc, error_msg):
    """
    Waits for a file to be created within a specified timeout. If the file is not found, it terminates the given process and fails the test.
     :param file_path: Path to the file to wait for
     :param timeout: Maximum time to wait in seconds
     :param cleanup_proc: subprocess.Popen object to terminate if file is not found
     :param error_msg: Error message to display if file is not found
    """
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            if cleanup_proc:
                cleanup_proc.terminate()
            pytest.fail(f"{error_msg} (File not found: {file_path})")
        time.sleep(0.5)
    return True


def wait_for_metrics_content(file_path, min_frames, timeout=20):
    """
    Waits for the metrics file to contain at least min_frames total_frames.
     :param file_path: Path to the metrics.json file
     :param min_frames: Minimum number of total_frames to wait for
     :param timeout: Maximum time to wait in seconds
     :return: Parsed JSON data if successful, None if timeout occurs
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    if data.get("total_frames", 0) >= min_frames:
                        return data
            except (json.JSONDecodeError, IOError):
                pass
        time.sleep(0.5)
    return None


def wait_for_data_growth(file_path, key="total_frames", wait_time=3, timeout=20):
    """
    Waits for a specific key in the JSON file to show growth after a wait time.
     :param file_path: Path to the JSON file to monitor
     :param key: The specific key in the JSON to monitor for growth
     :param wait_time: Time to wait before checking for growth (in seconds)
     :param timeout: Maximum time to wait for growth (in seconds)
     :return: Tuple (is_growing: bool, final_data: dict or None)
    """
    initial_data = wait_for_metrics_content(file_path, min_frames=1, timeout=timeout)
    if not initial_data:
        return False, None
    first_count = initial_data.get(key, 0)
    time.sleep(wait_time)
    try:
        with open(file_path, "r") as f:
            second_data = json.load(f)
            second_count = second_data.get(key, 0)

            if second_count > first_count:
                return True, second_data
    except Exception:
        pass

    return False, initial_data
