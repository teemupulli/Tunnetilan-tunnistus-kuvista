import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

from data_pipeline import create_datasets


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate emotion recognition model")
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--data_dir", default="dataset/raw")
    parser.add_argument("--split", choices=["test", "val"], default="test")
    parser.add_argument("--image_size", type=int, default=96)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--output_prefix", default="report/eval")
    return parser.parse_args()


def ensure_parent(output_prefix):
    Path(output_prefix).parent.mkdir(parents=True, exist_ok=True)


def main():
    args = parse_args()
    ensure_parent(args.output_prefix)

    _, val_ds, test_ds, class_names = create_datasets(
        args.data_dir,
        image_size=(args.image_size, args.image_size),
        batch_size=args.batch_size,
        augment=False,
    )

    dataset = test_ds if args.split == "test" else val_ds
    model = tf.keras.models.load_model(args.model_path)

    probabilities = model.predict(dataset)
    y_pred = np.argmax(probabilities, axis=1)

    y_true = np.concatenate([np.argmax(labels.numpy(), axis=1) for _, labels in dataset], axis=0)

    report = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    with open(f"{args.output_prefix}_classification_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    with open(f"{args.output_prefix}_classification_report.txt", "w", encoding="utf-8") as f:
        f.write(classification_report(y_true, y_pred, target_names=class_names, zero_division=0))

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title(f"Confusion Matrix ({args.split})")
    plt.tight_layout()
    plt.savefig(f"{args.output_prefix}_confusion_matrix.png")
    plt.close()


if __name__ == "__main__":
    main()
