import yfinance as yf
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import tensorflow

# Definizione del tuo portafoglio
stocks = {
    'VT': 10,
    'VYM': 10,
    'SONY': 5,
    'INTC': 5,
    'PG': 5,
    'ALB': 5,
    'KO': 10,
    'PEP': 5,
    'JNJ': 5,
    'IBM': 5,
}

bonds = {
    'SHY': 10,
    'GLD': 10,
    'BND': 5,
    'TLT': 10,
    'IEF': 5,
}

# Unisci tutti gli identificativi in una lista
all_symbols = list(stocks.keys()) + list(bonds.keys())

# Scarica i dati di tutti i titoli nel tuo portafoglio
data = yf.download(all_symbols, start="2020-01-01", end="2023-12-31")

# Preparazione dei dati e addestramento del modello LSTM per ogni titolo
for stock_name in all_symbols:
    stock_data = data['Close'][stock_name]
    stock_data = stock_data.values.reshape(-1, 1)

    scaler = MinMaxScaler()
    stock_data = scaler.fit_transform(stock_data)

    train_data = stock_data[:len(stock_data)-50]
    test_data = stock_data[len(stock_data)-50:]

    x_train = []
    y_train = []

    for i in range(50, len(train_data)):
        x_train.append(train_data[i-50:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

    # Salvare il modello
    model.save(os.path.join(os.getcwd(), f'{stock_name}_model.h5'))

# Ora, per ogni titolo nel tuo portafoglio, avrai un modello LSTM addestrato salvato come un file .h5 nella tua directory di lavoro corrente.
