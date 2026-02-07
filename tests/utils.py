import json
import os
import time
import pytest
import psutil 

def remove_file_if_exists(files):
    """
    Utility function to remove specified files if they exist.
     :param files: List of file paths to remove
    """
    for file_path in files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"[!] Error removing file {file_path}: {e}")
    
def kill_process_tree(parent_pid):
    """
    Kills a process and all of its child processes.
     :param parent_pid: PID of the parent process to kill
    """
    try:
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)
        for child in children:
            print(f"- Killing child process: {child.pid} ({child.name()})")
            child.kill()
        print(f"- Killing parent process: {parent.pid}")
        parent.kill()
    except psutil.NoSuchProcess:
        pass

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


def wait_for_metrics_content(file_path, min_frames=5, timeout=20):
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


def wait_for_data_growth(file_path,wait_time=2, timeout=25):
    """
    Waits for a total_frames count to grow in the metrics file, indicating that the system is actively processing frames.
    """
    key="total_frames"
    start_time = time.time()
    initial_data = wait_for_metrics_content(file_path)
    if not initial_data:
        return False, None
    
    first_count = initial_data[key]
    while time.time() - start_time < timeout:
        time.sleep(wait_time)      
        try:
            if os.path.exists(file_path):
                current_data = wait_for_metrics_content(file_path)
                current_count = current_data[key]                  
                if current_count > first_count:
                    print(f"[+] Growth detected! {first_count} -> {current_count}")
                    return True, current_data
        except (json.JSONDecodeError, IOError):
            continue           
    print(f"[!] Timeout: No growth detected for {key} after {timeout}s")
    return False, initial_data