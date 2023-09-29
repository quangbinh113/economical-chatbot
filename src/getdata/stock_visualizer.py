import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import json
from datetime import datetime, timezone
from matplotlib import pyplot as plt
import seaborn as sns

epoch_timestamp_now = int(datetime.now().timestamp())

class StockVisualization(object):
    """
    A class to visualize stock data.
    Data source: VNDIRECT API.
    """
    def __init__(self, symbol='FPT', resolution=1, start_date=epoch_timestamp_now, period=5) -> None:
        self.symbol = symbol
        self.resolution = resolution
        self.start_date = start_date
        self.end_date = start_date - (period * 365 * 24 * 60 * 60)
        self.VND_API = r'https://dchart-api.vndirect.com.vn/dchart/history'
        self.data_frame = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'dchart-api.vndirect.com.vn'
        }
        self.params = {
            'symbol': self.symbol,
            'resolution': self.resolution,
            'from': self.end_date,
            'to': self.start_date,
        }
    
    def __str__(self) -> str:
        return f'''StockVisualization(
            symbol={self.symbol}, resolution={self.resolution}, 
            start_date={self.start_date}, end_date={self.end_date}
        )'''
    
    def get_data(self) -> pd.DataFrame:
        """
        A function to get stock data from VNDIRECT API.
        Returns:
            data: (pd.DataFrame) -> A DataFrame containing stock data.
        """
        response = requests.get(self.VND_API, params=self.params, headers=self.header)
        data_json = response.json()
        data = pd.DataFrame(data_json)
        data['datetime'] = data['t'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc))
        # data = data.set_index('datetime')
        data = data.drop(['t', 's'], axis=1)
        data.rename(
            columns = {
                'o':'open', 'c':'close',
                'h':'Thigh', 'l': 'low', 
                'v': 'volumn'
            }, 
            inplace = True
        )
        self.data_frame = data
        return data
    
    def plot_data(self) -> None:
        """
        A function to plot stock data.
        Args:
            data: (pd.DataFrame) -> A DataFrame containing stock data.
        """
        df = self.get_data()
        fig = px.histogram(
            df, x='datetime', 
            y=['open','close'], 
            template='plotly_dark',
            color_discrete_sequence=['gold','snow'],
            title=f'{self.symbol} Stock Data'
            )
        fig.show()
        
    

if __name__ == "__main__":
    df = StockVisualization()
    data = df.get_data()
    data.to_csv('stock_data.csv', index=False)
    df.plot_data()