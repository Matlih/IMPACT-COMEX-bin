# NCNN Export Guide

This guide describes how to convert YOLO checkpoints into NCNN format for low-latency edge inference. NCNN artifacts are optimized for constrained hardware and are suitable for Raspberry Pi deployment where CPU efficiency is critical.

## Why Export to NCNN
- Reduces runtime overhead for on-device inference.
- Produces deployment-friendly artifacts (`model.ncnn.param`, `model.ncnn.bin`, metadata).
- Aligns with the repository layout under `models/*_ncnn_model/`.

## Prerequisites
- Python environment with `ultralytics` installed.
- Source model checkpoints available in `models/`.

## Export Commands
Run from the repository root:

```sh
yolo export model=models/COMEX_bin.pt format=ncnn imgsz=640
```

## Output Expectations
After export, each model should generate an NCNN directory with files similar to:
- `metadata.yaml`
- `model.ncnn.param`
- `model.ncnn.bin`

In this project, the expected output folder include:
- `models/COMEX_bin_ncnn_model/`

## Validation
Perform a quick file-level validation after export:

```sh
ls models/*_ncnn_model
```

If each folder contains both `.param` and `.bin`, the export step is complete.

## Troubleshooting
- Export fails with missing dependencies: confirm `ultralytics` and `ncnn` are installed in the active environment.
- Incorrect path errors: run commands from repository root so `models/...` paths resolve correctly.
- Inference mismatch: keep export image size (`imgsz=640`) consistent with your runtime preprocessing settings.