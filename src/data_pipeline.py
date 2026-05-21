from pathlib import Path

import tensorflow as tf


def verify_directory_structure(data_dir):
    data_path = Path(data_dir)
    expected_splits = ["train", "val", "test"]

    for split in expected_splits:
        split_path = data_path / split
        if not split_path.exists():
            raise FileNotFoundError(f"Missing split directory: {split_path}")


def create_datasets(data_dir, image_size=(96, 96), batch_size=32, augment=True, seed=123):
    verify_directory_structure(data_dir)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        Path(data_dir) / "train",
        image_size=image_size,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=True,
        seed=seed,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        Path(data_dir) / "val",
        image_size=image_size,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=False,
    )

    test_ds = tf.keras.utils.image_dataset_from_directory(
        Path(data_dir) / "test",
        image_size=image_size,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=False,
    )

    class_names = train_ds.class_names

    if augment:
        augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.08),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.RandomContrast(0.1),
            tf.keras.layers.RandomTranslation(0.05, 0.05),
        ], name="augmentation")

        train_ds = train_ds.map(
            lambda x, y: (augmentation(x, training=True), y),
            num_parallel_calls=tf.data.AUTOTUNE,
        )

    normalization = tf.keras.layers.Rescaling(1.0 / 255)

    train_ds = train_ds.map(lambda x, y: (normalization(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (normalization(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    test_ds = test_ds.map(lambda x, y: (normalization(x), y), num_parallel_calls=tf.data.AUTOTUNE)

    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)
    test_ds = test_ds.prefetch(tf.data.AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names
