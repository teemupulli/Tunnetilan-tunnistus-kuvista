import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf


def parse_args():
    parser = argparse.ArgumentParser(description="Run emotion recognition inference for a single image")
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--class_names", nargs="+", required=True)
    parser.add_argument("--image_size", type=int, default=96)
    return parser.parse_args()


def load_image(image_path, image_size):
    image = tf.keras.utils.load_img(image_path, target_size=(image_size, image_size))
    array = tf.keras.utils.img_to_array(image) / 255.0
    return np.expand_dims(array, axis=0)


def main():
    args = parse_args()
    if not Path(args.image_path).exists():
        raise FileNotFoundError(f"Image not found: {args.image_path}")

    model = tf.keras.models.load_model(args.model_path)
    image = load_image(args.image_path, args.image_size)
    probabilities = model.predict(image, verbose=0)[0]
    best_index = int(np.argmax(probabilities))

    print("Predicted class:", args.class_names[best_index])
    print("Confidence:", float(probabilities[best_index]))

    for class_name, score in zip(args.class_names, probabilities):
        print(f"{class_name}: {float(score):.4f}")


if __name__ == "__main__":
    main()
