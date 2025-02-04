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
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
#

def build_encoder(latent_dim):
    inputs = layers.Input(shape=(28, 28, 1))  # Example: 28x28 grayscale images
    x = layers.Conv2D(32, 3, activation='relu', strides=2, padding='same')(inputs)
    x = layers.Conv2D(64, 3, activation='relu', strides=2, padding='same')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)

    # Latent space: mean and log variance
    mu = layers.Dense(latent_dim, name='mu')(x)
    log_var = layers.Dense(latent_dim, name='log_var')(x)

    encoder = models.Model(inputs, [mu, log_var], name="encoder")
    return encoder


def build_decoder(latent_dim):
    latent_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(7 * 7 * 64, activation='relu')(latent_inputs)
    x = layers.Reshape((7, 7, 64))(x)
    x = layers.Conv2DTranspose(64, 3, activation='relu', strides=2, padding='same')(x)
    x = layers.Conv2DTranspose(32, 3, activation='relu', strides=2, padding='same')(x)
    outputs = layers.Conv2DTranspose(1, 3, activation='sigmoid', padding='same')(x)

    decoder = models.Model(latent_inputs, outputs, name="decoder")
    return decoder


def sampling(args):
    mu, log_var = args
    batch = tf.shape(mu)[0]
    dim = tf.shape(mu)[1]

    epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
    z = mu + tf.exp(0.5 * log_var) * epsilon  # Reparameterization trick
    return z


def build_vae(latent_dim):
    encoder = build_encoder(latent_dim)
    decoder = build_decoder(latent_dim)

    inputs = layers.Input(shape=(28, 28, 1))  # Example: 28x28 grayscale images
    noisy_inputs = layers.GaussianNoise(0.1)(inputs)  # Add noise to the input

    # Encode the noisy input
    mu, log_var = encoder(noisy_inputs)
    z = layers.Lambda(sampling)([mu, log_var])

    # Decode the latent variable
    reconstructed = decoder(z)

    vae = models.Model(inputs, reconstructed, name="vae")
    vae.encoder = encoder
    vae.decoder = decoder
    return vae, encoder, decoder


def vae_loss(x, x_reconstructed, mu, log_var):
    # Reconstruction loss
    reconstruction_loss = tf.reduce_mean(
        tf.reduce_sum(tf.keras.losses.binary_crossentropy(x, x_reconstructed), axis=(1, 2))
    )

    # KL divergence loss
    kl_loss = -0.5 * tf.reduce_mean(
        tf.reduce_sum(1 + log_var - tf.square(mu) - tf.exp(log_var), axis=0)
    )

    return reconstruction_loss + kl_loss


# Generate denoised images
def plot_denoised_images(vae, x_test):
    noisy_images = x_test + np.random.normal(0, 0.1, size=x_test.shape)
    noisy_images = np.clip(noisy_images, 0., 1.)  # Clip to valid range

    denoised_images = vae.predict(noisy_images)

    # Plot some images
    n = 10  # Number of images to display
    plt.figure(figsize=(20, 4))
    for i in range(n):
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(noisy_images[i].reshape(28, 28), cmap="gray")
        plt.title("Noisy")
        plt.axis("off")

        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(denoised_images[i].reshape(28, 28), cmap="gray")
        plt.title("Denoised")
        plt.axis("off")
    plt.show()


class DVAAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90561-8-010-3 Algo\n", dic, '\n', '-'*50)
        try:
            super(DVAAlgo, self).__init__()
        except Exception as ex:
            print("Error AES 9057-010-9 Algo:\n"+str(ex), "\n", '-'*50)

        self.app = dic["app"]


class DVADP(BaseDataProcessing, BasePotentialAlgo, DVAAlgo):
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
        print("90188-dva-1: \n", "="*50, "\n", dic, "\n", "="*50)
        # epochs = int(dic["epochs"])

        latent_dim = 2  # Dimensionality of the latent space

        # Build VAE model
        vae, encoder, decoder = build_vae(latent_dim)

        # Compile the model
        vae.compile(optimizer='adam', loss=lambda x, y: vae_loss(x, y, *vae.encoder(x)))

        # Load dataset (e.g., MNIST)
        (x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
        x_train = np.expand_dims(x_train, -1).astype("float32") / 255.0
        x_test = np.expand_dims(x_test, -1).astype("float32") / 255.0

        # Train the VAE
        vae.fit(x_train, x_train, epochs=1, batch_size=128)

        # Visualize denoised images
        plot_denoised_images(vae, x_test)


        result = {"status": "ok dva train", "data":{}}
        return result


