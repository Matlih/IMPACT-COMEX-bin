# pigpio GPIO Service Guide

This guide documents a stable `pigpio` setup for Project IMPACT-COMEX hardware actuation. The service is required for precise GPIO control across servo, LED, buzzer, and sensor components on Raspberry Pi.

## Why pigpio
- Provides low-jitter GPIO timing suitable for servo pulse control.
- Runs as a background daemon (`pigpiod`) that Python code can connect to.
- Improves reliability for continuous edge workloads.

## 1) Build and Install pigpio

```sh
sudo apt-get update
sudo apt install -y git build-essential
git clone https://github.com/joan2937/pigpio.git
cd pigpio
make
sudo make install
```

## 2) Start the Daemon

```sh
sudo pigpiod
```

## 3) Verify Service Health
Check that the daemon process is running:

```sh
pgrep pigpiod
```

If a PID is returned, the daemon is active and GPIO clients can connect.

## 4) Optional: Enable Auto-Start at Boot
For unattended deployment, enable `pigpiod` as a system service:

```sh
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
sudo systemctl status pigpiod
```

## Troubleshooting
- `Can't connect to pigpio`: confirm daemon is running before starting the Python app.
- Servo not moving: verify GPIO pin mapping and power integrity for external actuators.
- Permission issues: run hardware setup commands with `sudo` and avoid mixed user/system installs.