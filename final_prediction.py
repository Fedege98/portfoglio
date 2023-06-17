import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model

# Definizione del tuo portafoglio
stocks = {
    'VT': 0.10,
    'VYM': 0.10,
    'SONY': 0.05,
    'INTC': 0.05,
    'PG': 0.05,
    'ALB': 0.05,
    'KO': 0.10,
    'PEP': 0.05,
    'JNJ': 0.05,
    'IBM': 0.05,
}

bonds = {
    'SHY': 0.10,
    'GLD': 0.10,
    'BND': 0.05,
    'TLT': 0.10,
    'IEF': 0.05,
}

# Unisci tutti gli identificativi in una lista
all_symbols = list(stocks.keys()) + list(bonds.keys())

# Scarica i dati di tutti i titoli nel tuo portafoglio
data = yf.download(all_symbols, start="2020-01-01", end="2024-12-31")

portfolio_value = 10000  # Valore totale del tuo portafoglio

for year in range(5):
    # Carica i modelli e fai le previsioni
    predicted_portfolio_value = 0
    for stock_name in all_symbols:
        stock_data = data['Close'][stock_name]
        stock_data = stock_data.values.reshape(-1, 1)

        scaler = MinMaxScaler()
        stock_data = scaler.fit_transform(stock_data)

        model = load_model(f'models/{stock_name}_model.h5')
        x_input = stock_data[-50:]
        x_input = x_input.reshape((1, -1, 1))

        prediction = model.predict(x_input)
        predicted_price = scaler.inverse_transform(prediction)

        current_price = data['Close'][stock_name].iloc[-1]  # Prezzo più recente

        number_of_shares = portfolio_value * (stocks[stock_name] if stock_name in stocks else bonds[stock_name]) / current_price
        predicted_portfolio_value += number_of_shares * predicted_price

    # Calcola il rendimento previsto come percentuale di cambiamento nel valore del portafoglio
    expected_return = ((predicted_portfolio_value - portfolio_value) / portfolio_value) * 100
    print(f"Il rendimento previsto del portafoglio nel {year+1}° anno è: {expected_return}%")
    
    # Aggiorna il valore del portafoglio per il prossimo anno
    portfolio_value = predicted_portfolio_value
