import yfinance as yf
import pandas as pd

# функция поиска границ
def calculates_outliners(data):
    q25 = data.quantile(0.25)
    q75 = data.quantile(0.75)
    iqr = q75 - q25
    bound = (q25 - 1.5 * iqr, q75 + 1.5 * iqr)
    return bound 

# замена аномальных значений на вычесленные отрезки
def swap_anomaly(df, is_outliner, name_col, bound):
    return df.loc[is_outliner, name_col].apply(lambda x: bound[0] if x < 0 else bound[1])

#получение данных тикера
def get_ticker(ticker_name, period, interval):
    
    ticker = yf.download(ticker_name, period=period, interval=interval)
    df_ticker = pd.DataFrame(ticker)
    
    # добавление нового столбца для поиска аномалий при помощи изменения цены закрытия
    df_ticker['changes'] = (df_ticker['Close'] / df_ticker['Close'].shift(1) -1)*100
    df_ticker['changes'] = df_ticker['changes'].fillna(0)
    
    return df_ticker
