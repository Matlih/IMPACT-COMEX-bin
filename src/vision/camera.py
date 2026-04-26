import sys
import cv2

def init_camera(config):
    camera_backend = cv2.CAP_V4L2 if sys.platform.startswith("linux") else cv2.CAP_ANY
    camera = cv2.VideoCapture(config["cameraIndex"], camera_backend)

    if config.get("cameraWidth"):
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, config["cameraWidth"])
    if config.get("cameraHeight"):
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config["cameraHeight"])
    if config.get("cameraFps"):
        camera.set(cv2.CAP_PROP_FPS, config["cameraFps"])
    if config.get("cameraBufferSize") is not None:
        camera.set(cv2.CAP_PROP_BUFFERSIZE, config["cameraBufferSize"])

    if not camera.isOpened():
        raise RuntimeError(f"Unable to open camera {config['cameraIndex']}")

    return camera
