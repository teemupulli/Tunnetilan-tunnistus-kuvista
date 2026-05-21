import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import tensorflow as tf

from data_pipeline import create_datasets
from models import build_model


def parse_args():
    parser = argparse.ArgumentParser(description="Train emotion recognition models")
    parser.add_argument("--mode", choices=["cnn", "feature", "finetune"], default="cnn")
    parser.add_argument("--data_dir", default="dataset/raw")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--image_size", type=int, default=96)
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--unfrozen_layers", type=int, default=20)
    parser.add_argument("--output_dir", default="models")
    return parser.parse_args()


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def plot_history(history, output_prefix):
    history_dict = history.history

    plt.figure()
    plt.plot(history_dict["accuracy"], label="train")
    plt.plot(history_dict["val_accuracy"], label="val")
    plt.title("Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_accuracy.png")
    plt.close()

    plt.figure()
    plt.plot(history_dict["loss"], label="train")
    plt.plot(history_dict["val_loss"], label="val")
    plt.title("Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_loss.png")
    plt.close()

    with open(f"{output_prefix}_history.json", "w", encoding="utf-8") as f:
        json.dump(history_dict, f, indent=2)


def main():
    args = parse_args()
    ensure_dir(args.output_dir)

    train_ds, val_ds, test_ds, class_names = create_datasets(
        args.data_dir,
        image_size=(args.image_size, args.image_size),
        batch_size=args.batch_size,
        augment=True,
    )

    model = build_model(
        mode=args.mode,
        input_shape=(args.image_size, args.image_size, 3),
        num_classes=len(class_names),
        unfrozen_layers=args.unfrozen_layers,
    )

    learning_rate = args.learning_rate
    if args.mode == "finetune" and learning_rate >= 1e-3:
        learning_rate = 1e-4

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model_path = Path(args.output_dir) / f"{args.mode}_best.keras"
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(model_path),
            monitor="val_loss",
            save_best_only=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
        ),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks,
    )

    results = model.evaluate(test_ds, verbose=1)
    print("Test loss:", results[0])
    print("Test accuracy:", results[1])
    print("Class names:", class_names)

    plot_prefix = Path(args.output_dir) / args.mode
    plot_history(history, str(plot_prefix))


if __name__ == "__main__":
    main()
