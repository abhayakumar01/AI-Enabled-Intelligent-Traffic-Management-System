from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


CLASS_NAMES = ["truck", "accident", "van", "car", "bike", "bus"]
PROJECT_ROOT = Path(__file__).resolve().parent


def validate_dataset(dataset_root: Path) -> None:
    required = [
        dataset_root / "images" / "train",
        dataset_root / "images" / "val",
        dataset_root / "labels" / "train",
        dataset_root / "labels" / "val",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Dataset is missing required YOLO folders:\n" + "\n".join(missing)
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the six-class accident detector.")
    parser.add_argument("--data", default=str(PROJECT_ROOT / "accident_dataset.yaml"))
    parser.add_argument(
        "--dataset-root",
        default=None,
        help="Dataset folder containing images/train, images/val, labels/train, and labels/val.",
    )
    parser.add_argument("--model", default="yolov8s.pt")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=960)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--device", default=None, help="Use 0 for CUDA or cpu.")
    args = parser.parse_args()

    data_path = Path(args.data).resolve()
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {data_path}")
    dataset_root = (
        Path(args.dataset_root).resolve()
        if args.dataset_root
        else data_path.parent / "datasets" / "accident"
    )
    validate_dataset(dataset_root)

    model = YOLO(args.model)
    train_kwargs = {
        "data": str(data_path),
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "project": "runs/accident",
        "name": "yolov8s_accident",
        "patience": 25,
        "pretrained": True,
        "plots": True,
    }
    if args.device:
        train_kwargs["device"] = args.device
    model.train(**train_kwargs)
    print("Training complete. Copy runs/accident/yolov8s_accident/weights/best.pt to accident_best.pt")


if __name__ == "__main__":
    main()
