import os

from twisted.mail.smtp import xtext_codec

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import numpy as np
from datetime import datetime
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
#
from ..basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from ....core.utils import log_debug, clear_log_debug
#
from ....core.utils import log_debug, clear_log_debug
#

import tensorflow as tf
from tensorflow.keras import layers, Model, backend as K
from tensorflow.keras.datasets import mnist


# Encoder
class Encoder(Model):
    def __init__(self, latent_dim):
        super(Encoder, self).__init__()
        self.conv1 = layers.Conv2D(32, 3, activation="relu", strides=2, padding="same")
        self.conv2 = layers.Conv2D(64, 3, activation="relu", strides=2, padding="same")
        self.flatten = layers.Flatten()
        self.dense_mu = layers.Dense(latent_dim)  # Mean of latent space
        self.dense_log_var = layers.Dense(latent_dim)  # Log variance of latent space

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.flatten(x)
        mu = self.dense_mu(x)
        log_var = self.dense_log_var(x)
        return mu, log_var

# Sampling layer
class Sampling(layers.Layer):
    def call(self, inputs):
        mu, log_var = inputs
        batch = tf.shape(mu)[0]
        dim = tf.shape(mu)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return mu + tf.exp(0.5 * log_var) * epsilon

# Decoder
class Decoder(Model):
    def __init__(self, input_shape):
        super(Decoder, self).__init__()
        self.dense = layers.Dense(7 * 7 * 64, activation="relu")
        self.reshape = layers.Reshape((7, 7, 64))
        self.conv2d_transpose1 = layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")
        self.conv2d_transpose2 = layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")
        self.conv2d_transpose3 = layers.Conv2DTranspose(1, 3, activation="sigmoid", padding="same")

    def call(self, inputs):
        x = self.dense(inputs)
        x = self.reshape(x)
        x = self.conv2d_transpose1(x)
        x = self.conv2d_transpose2(x)
        return self.conv2d_transpose3(x)

# VAE Model
class VAE(Model):
    def __init__(self, encoder, decoder):
        super(VAE, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.sampling = Sampling()

    def call(self, inputs):
        mu, log_var = self.encoder(inputs)
        z = self.sampling([mu, log_var])
        reconstructed = self.decoder(z)
        return reconstructed, mu, log_var

# Loss function
def vae_loss(x, x_reconstructed, mu, log_var):
    reconstruction_loss = tf.reduce_mean(
        tf.reduce_sum(
            tf.keras.losses.binary_crossentropy(x, x_reconstructed), axis=(1, 2)
        )
    )
    kl_loss = -0.5 * tf.reduce_mean(
        tf.reduce_sum(1 + log_var - tf.square(mu) - tf.exp(log_var), axis=0)
    )
    return reconstruction_loss + kl_loss

# # Generate and visualize new samples
# import matplotlib.pyplot as plt
#
# def plot_latent_space(vae, n=30, figsize=15):
#     """Plots 2D latent space by decoding grid of sampled points."""
#     digit_size = 28
#     scale = 2.0
#     figure = np.zeros((digit_size * n, digit_size * n))
#     grid_x = np.linspace(-scale, scale, n)
#     grid_y = np.linspace(-scale, scale, n)
#
#     for i, yi in enumerate(grid_y):
#         for j, xi in enumerate(grid_x):
#             z_sample = np.array([[xi, yi]])
#             x_decoded = vae.decoder.predict(z_sample)
#             digit = x_decoded[0].reshape(digit_size, digit_size)
#             figure[
#                 i * digit_size : (i + 1) * digit_size,
#                 j * digit_size : (j + 1) * digit_size,
#             ] = digit
#
#     plt.figure(figsize=(figsize, figsize))
#     plt.imshow(figure, cmap="Greys_r")
#     plt.axis("off")
#     plt.show()
#
# plot_latent_space(vae)




########################################################
class VAEAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90561-8-010-3 Algo\n", dic, '\n', '-'*50)
        try:
            super(VAEAlgo, self).__init__()
        except Exception as ex:
            print("Error AES 9057-010-9 Algo:\n"+str(ex), "\n", '-'*50)

        self.app = dic["app"]


class VAEDP(BaseDataProcessing, BasePotentialAlgo, VAEAlgo):
    def __init__(self, dic):
        # print("90567-010 DataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)
        self.PATH = os.path.join(self.TO_OTHER, "aes")
        os.makedirs(self.PATH, exist_ok=True)
        # print(f'{self.PATH}')
        clear_log_debug()
        #

    # For Simple one independent variable.
    def train(self, dic):
        print("90155-vae-1: \n", "="*50, "\n", dic, "\n", "="*50)
        # epochs = int(dic["epochs"])

        # Load MNIST dataset
        (x_train, _), (x_test, _) = mnist.load_data()
        x_train = x_train.astype("float32") / 255.0
        x_test = x_test.astype("float32") / 255.0
        x_train = np.reshape(x_train, (-1, 28, 28, 1))
        x_test = np.reshape(x_test, (-1, 28, 28, 1))

        # Model parameters
        input_shape = (28, 28, 1)
        latent_dim = 2  # Size of the latent space

        # Instantiate and compile the model
        encoder = Encoder(latent_dim)
        decoder = Decoder(input_shape)
        vae = VAE(encoder, decoder)

        vae.compile(optimizer=tf.keras.optimizers.Adam(), loss=lambda x, y: vae_loss(x, y[0], y[1], y[2]))

        # Train the model
        vae.fit(x_train, x_train, epochs=1, batch_size=128, validation_data=(x_test, x_test))

        result = {"status": "ok vae train", "data":{}}
        return result


