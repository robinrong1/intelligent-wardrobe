import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow.python.ops.numpy_ops.np_config as np_config
np_config.enable_numpy_behavior()

data, metadata = tfds.load('fashion_mnist', as_supervised=True, with_info=True)

training_data, testing_data = data['train'], data['test']

name_classes = metadata.features['label'].names

def normalize(images, labels):
    images = tf.cast(images, tf.float32)
    images /= 255
    return images, labels

training_data = training_data.map(normalize)
testing_data = testing_data.map(normalize)

training_data = training_data.cache()
testing_data = testing_data.cache()

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28,1)),
    tf.keras.layers.Dense(50, activation=tf.nn.relu),
    tf.keras.layers.Dense(50, activation=tf.nn.relu),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

num_training_data = metadata.splits["train"].num_examples
num_test_data = metadata.splits["test"].num_examples
BATCH = 32

training_data = training_data.repeat().shuffle(num_training_data).batch(BATCH)
testing_data = testing_data.batch(BATCH)

import matplotlib.pyplot as plt

def classify_clothing(image):
    # Resize the image to 28x28
    image = tf.image.resize(image, [28, 28])
    
    # Reshape the image and normalize it
    image = tf.reshape(image, shape=(1, 28, 28, 1))  # Reshape to match the model input
    image = tf.cast(image, tf.float32) / 255.0  # Normalize the image

    # Perform prediction
    predictions = model.predict(image)
    predicted_class = tf.argmax(predictions, axis=1).numpy()[0]

    class_names = metadata.features['label'].names

    # Display prediction result
    return class_names[predicted_class]

if __name__ == '__main__':
    image = tf.io.read_file('./Clothes/sweater.png')
    image = tf.image.decode_png(image, channels=1)  # Load the image in grayscale

    print(classify_clothing(image))
