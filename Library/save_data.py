import pandas as pd

def save_data(df, ticker, period, interval, df_anomaly = pd.DataFrame()):
        if not df_anomaly.empty:
                df.to_csv(f'Data/{ticker}_{period}_{interval}.csv')
        
                df_anomaly.to_csv(f'Data/{ticker}_{period}_{interval}_anomaly.csv')
        else:
                df.to_csv(f'Data/{ticker}_{period}_{interval}.csv')

