import pandas as pd
import numpy as np

class MeanReversionMomentumStrategy:
    def __init__(self, momentum_period=50, rsi_period=14, rsi_oversold=40, rsi_overbought=60):
        self.momentum_period = momentum_period
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought

    def calculate_indicators(self, df):
        """
        Calculate SMA and RSI indicators.
        Expected df columns: 'intc' (Close price)
        """
        df = df.copy()
        
        # Ensure 'intc' is numeric
        df['intc'] = pd.to_numeric(df['intc'], errors='coerce')
        
        # Momentum: Simple Moving Average (SMA)
        df['sma'] = df['intc'].rolling(window=self.momentum_period).mean()
        
        # Mean Reversion: Relative Strength Index (RSI)
        delta = df['intc'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        return df

    def generate_signals(self, df):
        """
        Generate Buy/Sell signals based on strategy logic.
        """
        df = self.calculate_indicators(df)
        df['signal'] = 0
        
        # Buy Signal: Uptrend (Close > SMA) AND Oversold (RSI < 40)
        buy_condition = (df['intc'] > df['sma']) & (df['rsi'] < self.rsi_oversold)
        
        # Sell Signal: Downtrend (Close < SMA) AND Overbought (RSI > 60)
        sell_condition = (df['intc'] < df['sma']) & (df['rsi'] > self.rsi_overbought)
        
        df.loc[buy_condition, 'signal'] = 1
        df.loc[sell_condition, 'signal'] = -1
        
        return df
