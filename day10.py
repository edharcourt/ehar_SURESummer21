# CNN on real images (dogs vs cats) with transfer learning and data augmentation
from tensorflow import keras

# Generate and augment the training data
train_gen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1/255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
).flow_from_directory("train",
    target_size=(150, 150),
    batch_size=20,
    class_mode="binary"
)

# Generate the validation data
val_gen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1/255
).flow_from_directory("val",
    target_size=(150, 150),
    batch_size=20,
    class_mode="binary"
)

# Generate the testing data
test_gen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1/255
).flow_from_directory("test",
    target_size=(150, 150),
    batch_size=20,
    class_mode="binary"
)

# Load a pre-trained base network
base = keras.applications.VGG16(
    weights="imagenet",
    include_top=False,
    input_shape=(150, 150, 3)
)

# Freeze the base
base.trainable = False

# Add a new top
network = keras.models.Sequential()
network.add(base)
network.add(keras.layers.Flatten())
network.add(keras.layers.Dense(64, activation="relu"))
network.add(keras.layers.Dense(1, activation="sigmoid"))

# Train the new top
network.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

network.fit(train_gen,
    epochs=10,
    steps_per_epoch=100,
    validation_data=val_gen,
    validation_steps=50,
)

# Unfreeze the base
base.trainable = True

# Fine-tune the whole network
network.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.00001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

network.fit(train_gen,
    epochs=10,
    steps_per_epoch=100,
    validation_data=val_gen,
    validation_steps=50,
)

# Test the network
network.evaluate(test_gen, steps=50)

