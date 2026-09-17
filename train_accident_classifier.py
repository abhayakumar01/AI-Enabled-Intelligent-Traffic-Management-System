from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = PROJECT_ROOT / "datasets" / "accident" / "data"


def validate_dataset(dataset_root: Path) -> None:
    required = [dataset_root / "train", dataset_root / "val"]
    missing = [str(path) for path in required if not path.is_dir()]
    if missing:
        raise FileNotFoundError(
            "Classification dataset is missing required folders:\n" + "\n".join(missing)
        )

    for split in required:
        classes = [path for path in split.iterdir() if path.is_dir()]
        if len(classes) < 2:
            raise ValueError(f"{split} must contain at least two class folders.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the binary accident classifier.")
    parser.add_argument("--dataset-root", default=str(DEFAULT_DATASET))
    parser.add_argument("--model", default="yolov8s-cls.pt")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--imgsz", type=int, default=224)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default=None, help="Use 0 for CUDA or cpu.")
    args = parser.parse_args()

    dataset_root = Path(args.dataset_root).resolve()
    validate_dataset(dataset_root)

    model = YOLO(args.model)
    train_kwargs = {
        "data": str(dataset_root),
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "project": "runs/accident",
        "name": "yolov8s_accident_classifier",
        "patience": 10,
        "pretrained": True,
        "plots": True,
    }
    if args.device:
        train_kwargs["device"] = args.device
    model.train(**train_kwargs)
    print(
        "Training complete. Copy runs/accident/"
        "yolov8s_accident_classifier/weights/best.pt to accident_classifier.pt"
    )


if __name__ == "__main__":
    main()