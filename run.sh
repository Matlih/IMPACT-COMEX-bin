#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

VENV_DIR=".venv"
PYTHON_BIN="$VENV_DIR/bin/python"
MAIN_SCRIPT="main.py"
TEST_CAMERA_SCRIPT="tests/camera.py"
TEST_PIGPIO_SCRIPT="tests/pigpiod.py"
TEST_SERVO_SCRIPT="tests/servo.py"
TEST_SENSOR_SCRIPT="tests/sensor.py"
TEST_LED_SCRIPT="tests/led.py"
TEST_BUZZER_SCRIPT="tests/buzzer.py"
REQ_FILE="requirements/raspberrypi.txt"

pause_any() {
  read -r -n 1 -s -p "Press any key to continue..."
  echo
}

ensure_venv() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Creating virtual environment in $VENV_DIR ..."
    python3 -m venv --system-site-packages "$VENV_DIR" || {
      echo "Failed to create virtual environment."
      return 1
    }
  fi
  return 0
}

install_pigpio_from_source() {
  if command -v pigpiod >/dev/null 2>&1; then
    echo "pigpiod already installed. Skipping source build."
    return 0
  fi

  local pigpio_src_dir="/tmp/pigpio-src"
  echo "Downloading and building pigpio from source ..."
  rm -rf "$pigpio_src_dir"
  git clone --depth 1 https://github.com/joan2937/pigpio.git "$pigpio_src_dir" || return 1

  (
    cd "$pigpio_src_dir" || exit 1
    make || exit 1
    sudo make install || exit 1
  ) || return 1

  command -v pigpiod >/dev/null 2>&1
}

install_requirements() {
  echo "Installing OpenCV and related system packages (apt) ..."
  sudo apt-get update || return 1
  sudo apt-get install -y \
    python3-numpy \
    python3-opencv \
    python3-torch \
    python3-torchvision \
    git \
    build-essential \
    cmake \
    libgtk-3-dev \
    libboost-all-dev  || return 1

  install_pigpio_from_source || {
    echo "pigpio source install failed."
    return 1
  }

  if [ -d "$VENV_DIR" ] && [ ! -x "$PYTHON_BIN" ]; then
    echo "Existing virtual environment is invalid. Recreating $VENV_DIR ..."
    rm -rf "$VENV_DIR"
  fi

  if [ -x "$PYTHON_BIN" ]; then
    "$PYTHON_BIN" -c "import cv2" >/dev/null 2>&1 || {
      echo "Existing virtual environment cannot import cv2. Recreating with system-site-packages ..."
      rm -rf "$VENV_DIR"
    }
  fi

  ensure_venv || return 1
  echo "Installing dependencies from $REQ_FILE ..."
  "$PYTHON_BIN" -m pip install --upgrade pip
  "$PYTHON_BIN" -m pip install -r "$REQ_FILE"

  echo "Ensuring ultralytics stays compatible with system OpenCV ..."
  "$PYTHON_BIN" -m pip install --no-cache-dir --no-deps ultralytics
}

ensure_pigpiod_running() {
  if pgrep pigpiod >/dev/null 2>&1; then
    return 0
  fi

  echo "Enabling and starting pigpiod ..."
  if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl enable pigpiod >/dev/null 2>&1 || true
    sudo systemctl start pigpiod >/dev/null 2>&1 || sudo pigpiod >/dev/null 2>&1
  else
    sudo pigpiod >/dev/null 2>&1
  fi

  if pgrep pigpiod >/dev/null 2>&1; then
    return 0
  fi

  echo "Failed to start pigpiod. Please run: sudo pigpiod"
  return 1
}

run_main() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  ensure_pigpiod_running || return 1
  "$PYTHON_BIN" "$MAIN_SCRIPT"
}

run_main_headless() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  ensure_pigpiod_running || return 1
  "$PYTHON_BIN" "$MAIN_SCRIPT" --headless
}

run_camera_test() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  "$PYTHON_BIN" "$TEST_CAMERA_SCRIPT"
}

run_pigpio_test() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  ensure_pigpiod_running || return 1
  "$PYTHON_BIN" "$TEST_PIGPIO_SCRIPT"
}

run_servo_test() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  ensure_pigpiod_running || return 1
  "$PYTHON_BIN" "$TEST_SERVO_SCRIPT"
}

run_sensor_test() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  ensure_pigpiod_running || return 1
  "$PYTHON_BIN" "$TEST_SENSOR_SCRIPT"
}

run_led_test() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  ensure_pigpiod_running || return 1
  "$PYTHON_BIN" "$TEST_LED_SCRIPT"
}

run_buzzer_test() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Virtual environment not found. Run option 1 first."
    return 1
  fi
  ensure_pigpiod_running || return 1
  "$PYTHON_BIN" "$TEST_BUZZER_SCRIPT"
}

show_tests_menu() {
  while true; do
    clear || true
    echo "===== Tests Menu (Pi/Linux) ====="
    echo "1. Run camera test"
    echo "2. Run pigpio connection test"
    echo "3. Run servo test"
    echo "4. Run ultrasonic sensor test"
    echo "5. Run led output test"
    echo "6. Run buzzer output test"
    echo "0. Back"
    echo
    read -r -p "Enter option: " test_choice

    case "$test_choice" in
      1)
        run_camera_test
        pause_any
        ;;
      2)
        run_pigpio_test
        pause_any
        ;;
      3)
        run_servo_test
        pause_any
        ;;
      4)
        run_sensor_test
        pause_any
        ;;
      5)
        run_led_test
        pause_any
        ;;
      6)
        run_buzzer_test
        pause_any
        ;;
      0)
        return 0
        ;;
      *)
        echo "Invalid option. Please choose 0 to 6."
        pause_any
        ;;
    esac
  done
}

while true; do
  clear || true
  echo "===== Python Menu (Pi/Linux) ====="
  echo "1. Install requirements"
  echo "2. Run main.py"
  echo "3. Run main.py (headless)"
  echo "4. Tests menu"
  echo "0. Exit"
  echo
  read -r -p "Enter option: " choice

  case "$choice" in
    1)
      install_requirements
      pause_any
      ;;
    2)
      run_main
      pause_any
      ;;
    3)
      run_main_headless
      pause_any
      ;;
    4)
      show_tests_menu
      ;;
    0)
      echo "Exiting."
      exit 0
      ;;
    *)
      echo "Invalid option. Please choose 1, 2, 3, 4, or 0."
      pause_any
      ;;
  esac
done
