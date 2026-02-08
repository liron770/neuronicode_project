# QA Automation Home Assignment — RTP H264 Vehicle Detection 

A distributed system for real-time vehicle detection in video streams, utilizing RTP/SDP communication between a Sender and a Receiver.

# Project Structure

 tests/                  # Test suite directory
   - test_system.py      # Main integration tests
   - test_negative.py    # Edge case and failure handling tests
   - config.py           # Test environment configurations
   - utils.py            # Helper functions for tests 
 videoRoadTraffic.mp4    # Input video source
 cars.xml                # Haar Cascade model for vehicle detection
 Dockerfile              # Container configuration
 requirements.txt        # Python dependencies
 metrics.json            # Output file for system performance data
 sender.py               # Streams video frames via RTP using FFmpeg
 receiver.py             # Captures stream, runs AI detection, and logs metrics

# Project Overview

The system consists of two main microservices:
Sender: Reads a video file and streams it via RTP using FFmpeg.
Receiver: Captures the stream, performs image processing (OpenCV Haar Cascades) to detect vehicles, and generates real-time performance metrics exported to a JSON file.

# Visual AI Validation (Bounding Boxes)

The system doesn't just process data, it provides real-time visual feedback:
Dynamic Bounding Boxes: The Receiver draws green rectangles around every detected vehicle in the stream.
Frame-by-Frame Processing: Each frame is analyzed using the Haar Cascade model, and the coordinates are mapped instantly to the video display window.

# Execution Instructions

# Option 1: Running on Windows (Recommended for AI Validation)
To see the AI detection working with full accuracy, run the system natively:

Before running the system, ensure the following are installed and configured:

Python 3.10+: Ensure Python is added to your system PATH.
FFmpeg: The system relies on FFmpeg for RTP streaming.
Note: FFmpeg must be installed and the bin folder must be added to your System Environment Variables (PATH).

To verify, run ffmpeg -version in your terminal. If it's not recognized, the sender.py will fail to start.

#Install Dependencies:

# Bash
```
pip install -r requirements.txt
```
Run Tests:

# Bash
```
pytest -v
```

# Manual Run:

Start the Receiver: python receiver.py
Start the Sender: python sender.py

# Option 2: Running via Docker (Infrastructure Validation)
To verify the containerized environment and networking:

# Build the image
```
docker build -t vehicle-detection .
```

# Run automated suite
```
docker run -it --rm vehicle-detection pytest -v
```

# Challenges && Known Issues

1. AI Inference Discrepancy (Docker vs. Windows)
The Challenge: While the AI detection logic performs perfectly in a native Windows environment (achieving stable detection ratios), it encounters issues within the Docker container.
Despite the system architecture, networking, and metrics collection working as intended, the OpenCV Haar Cascade model often returns a 0.0 detection ratio inside the container.

Analysis: This discrepancy is likely due to how the headless Linux environment inside Docker handles video frame decoding or specific dependency versions for OpenCV/FFmpeg, which differ from the Windows host.

Current Status: The system is fully operational on Windows. In Docker, the infrastructure is validated and the pipeline is intact, but the AI model's sensitivity requires 
further environment-specific calibration.

2. Race Conditions in Automated Testing
The Challenge: The test suite executed faster than the FFmpeg stream initialization. This led to tests reading the metrics.json file before the AI had processed enough frames, resulting in false negatives.

The Solution: Developed a synchronization utility, wait_for_metrics_content, which uses a polling to wait for a minimum frame threshold before asserting results.

3. Process Management
The Challenge: Orphaned FFmpeg and Python processes remained active after test failures, locking UDP ports and causing subsequent runs to fail.

The Solution: Integrated the psutil library into the test teardown phase to recursively terminate all child processes, ensuring a clean environment for every test execution.

# Metrics Collected

The system generates a metrics.json report containing:

total_frames: Total frames processed by the Receiver.

detected_frames: Frames where at least one vehicle was found.

detection_ratio: Accuracy percentage.

avg_latency_ms: Average processing time per frame.

max_latency_ms: Peak processing time.

Example metrics.json output:
{
  "total_frames": 150,
  "detected_frames": 45,
  "detection_ratio": 0.3,
  "avg_latency_ms": 12.5,
  "max_latency_ms": 48.2
}


