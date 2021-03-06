#LSTM-AutoEncoder
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.utils import plot_model
from numpy import array
from keras.layers import Input
from keras.models import Model

#define input sequence
seq_in = array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

#reshape input into [samples, timesteps, features]
n_in = len(seq_in)
seq_in = seq_in.reshape((1, n_in, 1))

#prepare output sequence
seq_out = seq_in[:, 1:, :]
n_out = n_in - 1

#define encoder
visible = Input(shape=(n_in,1))
encoder = LSTM(100, activation='relu')(visible)

#Decoder 1 for prediction
decoder1 = RepeatVector(n_in)(encoder)
decoder1 = LSTM(100, activation='relu', return_sequences=True)(decoder1)
decoder1 = TimeDistributed(Dense(1))(decoder1)

#Decoder 2 for prediction
decoder2 = RepeatVector(n_out)(encoder)
decoder2 = LSTM(100, activation='relu', return_sequences=True)(decoder2)
decoder2 = TimeDistributed(Dense(1))(decoder2)

#tie up the encoder and the decoders
model = Model(inputs=visible, outputs=[decoder1, decoder2])
model.compile(optimizer='adam', loss='mse')

#fit model
model.fit(seq_in, [seq_in,seq_out], epochs=300, verbose=0)

#demonstrate prediction
results = model.predict(seq_in, verbose=1)
print(results)