import tensorflow as tf


def build_baseline_cnn(input_shape=(96, 96, 3), num_classes=7):
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu")(inputs)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(128, 3, padding="same", activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(256, 3, padding="same", activation="relu")(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    return tf.keras.Model(inputs, outputs, name="baseline_cnn")


def build_feature_extraction_model(input_shape=(96, 96, 3), num_classes=7):
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs * 255.0)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    return tf.keras.Model(inputs, outputs, name="mobilenetv2_feature")


def build_fine_tuned_model(input_shape=(96, 96, 3), num_classes=7, unfrozen_layers=20):
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet",
    )

    for layer in base_model.layers:
        layer.trainable = False

    if unfrozen_layers > 0:
        for layer in base_model.layers[-unfrozen_layers:]:
            if not isinstance(layer, tf.keras.layers.BatchNormalization):
                layer.trainable = True

    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs * 255.0)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    return tf.keras.Model(inputs, outputs, name="mobilenetv2_finetune")


def build_model(mode, input_shape=(96, 96, 3), num_classes=7, unfrozen_layers=20):
    if mode == "cnn":
        return build_baseline_cnn(input_shape=input_shape, num_classes=num_classes)
    if mode == "feature":
        return build_feature_extraction_model(input_shape=input_shape, num_classes=num_classes)
    if mode == "finetune":
        return build_fine_tuned_model(
            input_shape=input_shape,
            num_classes=num_classes,
            unfrozen_layers=unfrozen_layers,
        )
    raise ValueError(f"Unknown mode: {mode}")
