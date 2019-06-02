import os
import logging
from math import ceil
from keras.layers import Input, Dense
from keras.models import Model
from keras.backend import tf


class Autoencoder(object):

    def __init__(self, input_dim):
        self.input_dim = input_dim

    def init_layer_dims(self):
        self.latent_dim = ceil(self.input_dim/25)
        self.dim_2 = ceil(self.input_dim/10)
        self.dim_1 = ceil(self.input_dim/5)
        logging.info('Dimensions initialized')

    def init_model(self):
        input_ = Input(shape=(self.input_dim,))
        encoder = Dense(self.dim_1, activation='tanh')(input_)
        encoder = Dense(self.dim_2, activation='tanh')(encoder)
        encoder = Dense(self.latent_dim, activation='tanh')(encoder)

        decoder = Dense(self.dim_2, activation='tanh')(encoder)
        decoder = Dense(self.dim_1, activation='tanh')(decoder)
        decoder = Dense(self.input_dim, activation='sigmoid')(decoder)

        self.model = Model(input_, decoder)
        logging.info('Autoencoder model initialized')

    def fit_save(self, ae_config, data, model_folder):
        optimizer = self._retrieve_key(ae_config, 'optimizer')
        loss = self._retrieve_key(ae_config, 'loss')
        epochs = self._retrieve_key(ae_config, 'epochs')
        batch_size = self._retrieve_key(ae_config, 'batch_size')
        shuffle = self._retrieve_key(ae_config, 'shuffle')

        self.model.compile(optimizer=optimizer, loss=loss)
        self.model.fit(data, data,
                       epochs=epochs,
                       batch_size=batch_size,
                       shuffle=shuffle,
                       **ae_config)
        logging.info('Model fitted')
        model_path = os.path.join(model_folder, 'autoencoder.h5')
        self.model.save(model_path)
        logging.info(f'Model saved at {model_path}')

    def _retrieve_key(self, d, key):
        val = d[key]
        del d[key]
        return val
