# OpenCV Edge Runtime Guide

This guide documents a reproducible OpenCV runtime setup for Raspberry Pi deployments of Project IMPACT-COMEX. The objective is to keep inference fast and stable by combining system-level OpenCV packages with an isolated Python virtual environment.

## Runtime Strategy
- Install OpenCV and core numerical libraries from apt to leverage Raspberry Pi compatible binaries.
- Create a virtual environment with `--system-site-packages` so Python packages can reuse system OpenCV without rebuilding.
- Install `ultralytics` with `--no-deps` to avoid replacing optimized system packages.

## 1) Install System Dependencies
Run this on Raspberry Pi OS:

```sh
sudo apt-get update
sudo apt-get install -y python3-numpy python3-opencv python3-torch python3-torchvision build-essential cmake libgtk-3-dev libboost-all-dev plank compton
```

## 2) Create and Activate Virtual Environment
From the repository root:

```sh
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-cache-dir --no-deps ultralytics
```

## 3) Validate Installation
Use this quick check to verify OpenCV, PyTorch, and Ultralytics are available:

```sh
python -c "import cv2, torch, ultralytics; print('OpenCV:', cv2.__version__); print('Torch:', torch.__version__)"
```

If the command prints versions without errors, the environment is ready for camera inference and model execution.

## Troubleshooting
- `ModuleNotFoundError: cv2`: ensure `python3-opencv` was installed with apt and the virtual environment was created using `--system-site-packages`.
- Slow startup or install conflicts: keep `ultralytics` installed with `--no-deps` to avoid dependency overrides.
- Camera opens but no frames: verify USB camera permissions and confirm no other process is locking `/dev/video0`.