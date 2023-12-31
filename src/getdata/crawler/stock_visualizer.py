# ---------------------------------------------------------------------------
# project: vn_quant_update
# author: binh.truong
# date: 1st Jan 2023
# ---------------------------------------------------------------------------

import requests
import pandas as pd
import json
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
import seaborn as sns
import pytz
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
data_path = os.environ["DATA_PATH"]


class StockVisualization(object):
    """
    A class to visualize stock data.
    Data source: VNDIRECT API.
    REST API from candle stick chart OHLCV of each stock symbol in Vietnam stock market.
    """
    def __init__(
        self, symbol: str='FPT', 
        start_date=datetime.now(),
        end_date=datetime.now()-timedelta(days=7),
        ) -> None:
        """
        Class Attributes:
            symbol: (str) -> Stock symbol.
            resolution: (str) -> Time resolution, e.g., 1, D, W, M, Y.
            start_date: (datetime) -> Start date.
            end_date: (datetime) -> End date.
        """
        self.symbol = symbol
        # self.resolution = resolution
        self.start_date = start_date
        self.end_date = end_date
        self.VND_API = r'https://dchart-api.vndirect.com.vn/dchart/history'
        self.dataframe = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'dchart-api.vndirect.com.vn'
        }
        self.params = {
            'symbol': self.symbol,
            'resolution': None,
            'from': int(self.end_date.timestamp()),
            'to': int(self.start_date.timestamp()),
        }
    

    def __str__(self) -> str:
        return f'''StockVisualization(
            symbol={self.symbol}, resolution={self.resolution}, 
            start_date={self.start_date}, end_date={self.end_date}
        )'''


    def date_difference_description(self) -> str:
        """ 
        Calculate the difference between datetime1 and datetime2
        If the difference is less than a day, return 'hours'
        If the difference is less than a week, return 'days'
        If the difference is less than a year, return 'months'
        If the difference is more than a year, return 'years'
        ----------
        Args: 
            datetime1: datetime -> start date
            datetime2: datetime -> end date
        returns:
            str -> time marks
        """
        difference = relativedelta(self.start_date, self.end_date)
        
        if difference.years == 0 and difference.months == 0 and difference.days == 0:
            return 'hours'
        elif difference.years == 0 and difference.months == 0:
            return 'days'
        elif difference.years == 0:
            return 'months'
        else:
            return 'years'


    def get_data(self, params) -> pd.DataFrame:
        """
        A function to get stock data from VNDIRECT API.
        The data will be open, high, low, close, volume, and date.
        ------------
        Args:
            params: dict -> API parametters
        Returns:
            data: (pd.DataFrame) -> A DataFrame containing stock data.
        """
        def _get_date_time_from_timestamp(timestamp):
            return datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Bangkok'))

        response = requests.get(self.VND_API, params=params, headers=self.header)
        data_json = response.json()
        data = pd.DataFrame(data_json)
        data['Date'] = data['t'].apply(lambda x: _get_date_time_from_timestamp(x))
        # Convert price columns
        columns_to_convert = ['o', 'c', 'h', 'l']
        for column in columns_to_convert:
            data[column] = data[column].astype(float) * 1000
        # data = data.set_index('datetime')
        data = data.drop(['t', 's'], axis=1)
        data.rename(
            columns = {
                'o':'open', 'c':'close',
                'h':'high', 'l': 'low', 
                'v': 'volume'
            }, 
            inplace = True
        )
        self.data_frame = data
        return self.data_frame
    

    def plot_data(self) -> None:
        """
        A function to plot stock data.
        Library used: Plotly
        Style: Candlestick
        ------------
        Args:
            data: (pd.DataFrame) -> A DataFrame containing stock data.
        Returns:
            Interactive plotly chart: .html file
        """
        def _plot_daily_data(data: pd.DataFrame) -> None:
            """
            Plot daily data for time periods less than a month
            ------------
            Args:
                data: (pd.DataFrame) -> A DataFrame containing stock data.
            Returns:
                Interactive plotly chart: .html file
            """
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=data['Date'],
                        open=data['open'],
                        high=data['high'],
                        low=data['low'],
                        close=data['close'],
                        hovertext=[
                            f"Open: {open_}<br>Close: {close}<br>High: {high}<br>Low: {low}<br>Volume: {volume}"
                            for open_, close, high, low, volume in zip(
                                data['open'], 
                                data['close'], 
                                data['high'], 
                                data['low'], 
                                data['volume']
                            )
                        ],
                        hoverinfo="y",
                    )
                ]
            )
            # Update the layout to allow zooming by day, month, and hour
            fig.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1H", step="hour", stepmode="backward"),
                        dict(count=1, label="1D", step="day", stepmode="backward"),
                        dict(step="all")
                    ]),
                    bgcolor='lightgrey',  # Set the background color of the button area
                    activecolor='blue'  # Set the color of the active button
                ),
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                    dict(bounds=[14.30, 9.25], pattern="hour"),  # hide hours outside of 9.30am-3pm
                    dict(bounds=[11.30, 13], pattern="hour"),  # hide hours outside of 9.30am-4pm
                ]
            )
            fig.update_yaxes(type="log")
            fig.update_layout(
                xaxis_rangeslider_visible=False, 
                template='plotly_dark',
                xaxis_title='Date', 
                yaxis_title='Price', 
                title=self.symbol, 
                hovermode='x unified',
            )
            save_path = os.path.join(data_path, 'stock_visualization.html')
            fig.write_html(save_path)
            # fig.show()
        
        def _plot_yearly_data(data):
            """
            Plot yearly data for time periods more than a month
            ------------
            Args:
                data: (pd.DataFrame) -> A DataFrame containing stock data.
            Returns:
                Interactive plotly chart: .html file
            """
            data['20wma'] = data['close'].rolling(window=20).mean()
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=data['Date'],
                        open=data['open'],
                        high=data['high'],
                        low=data['low'],
                        close=data['close'],
                        hovertext=[
                            f"Open: {open_}<br>Close: {close}<br>High: {high}<br>Low: {low}<br>Volume: {volume}"
                            for open_, close, high, low, volume in zip(
                                data['open'], 
                                data['close'], 
                                data['high'], 
                                data['low'], 
                                data['volume']
                            )
                        ],
                        hoverinfo="y",
                    )
                ]
            )
            fig.add_trace(
                go.Scatter(
                    x=data['Date'],
                    y=data['20wma'],
                    name='20 week ma',
                    line=dict(color='grey', width=2, dash='dash')
                )
            )
            # Update the layout to allow zooming by day, month, and hour
            fig.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(step="all")
                    ]),
                    bgcolor='lightgrey',  # Set the background color of the button area
                    activecolor='blue'  # Set the color of the active button
                ),
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                ]
            )
            fig.update_yaxes(type="log")
            fig.update_layout(
                xaxis_rangeslider_visible=False, 
                template='plotly_dark',
                xaxis_title='Date', 
                yaxis_title='Price', 
                title=self.symbol, 
                hovermode='x unified',
            )
            save_path = os.path.join(data_path, 'stock_visualization.html')
            fig.write_html(save_path)
            # fig.show()

        # get plot based on time periods
        time_mark = self.date_difference_description()
        params = self.params

        # Classify time periods to decide the resolution -> daily or yearly type of plot
        if time_mark == 'hours' or time_mark == 'days':
            params['resolution'] = '1'
            self.get_data(params=params)
            _plot_daily_data(self.data_frame)
        else:
            params['resolution'] ='D'
            self.get_data(params=params)
            _plot_yearly_data(self.data_frame)



if __name__ == "__main__":
    df = StockVisualization('HPG', datetime.now(), datetime.now()-timedelta(days=5))
    # params = {
    #     'symbol': 'VNM',
    #     'resolution': '1',
    #     'to': int(datetime.now().timestamp()),
    #     'from': int((datetime.now() - timedelta(days=365)).timestamp()),
    # }
    # data = df.get_data(params=params)
    # data.to_csv('stock_data.csv', index=False)
    df.plot_data()

    # print(os.environ.get("OPENAI_API_KEY"))