import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []
        self.equity_curve = []

    def run(self, df, strategy):
        """
        Run backtest on the provided DataFrame using the given strategy.
        """
        df = strategy.generate_signals(df)
        
        # Iterate through data to simulate trading
        for i in range(1, len(df)):
            current_bar = df.iloc[i]
            prev_bar = df.iloc[i-1]
            
            # Check for signals
            if self.position == 0:
                if prev_bar['signal'] == 1: # Buy Signal
                    self.buy(current_bar['time'], current_bar['intc'])
                elif prev_bar['signal'] == -1: # Sell Signal
                    self.sell(current_bar['time'], current_bar['intc'])
            
            # Check for exit (Simple exit: RSI Neutral or Signal Reversal)
            # For simplicity in this example, we exit if signal reverses or RSI crosses 50
            elif self.position > 0: # Long Position
                if prev_bar['rsi'] > 50 or prev_bar['signal'] == -1:
                    self.close_position(current_bar['time'], current_bar['intc'])
            
            elif self.position < 0: # Short Position
                if prev_bar['rsi'] < 50 or prev_bar['signal'] == 1:
                    self.close_position(current_bar['time'], current_bar['intc'])
            
            # Track equity
            current_equity = self.capital + (self.position * (current_bar['intc'] - self.entry_price) if self.position != 0 else 0)
            self.equity_curve.append({'time': current_bar['time'], 'equity': current_equity})

        return self.get_performance_report()

    def buy(self, time, price):
        self.position = 1 # Simplified: 1 unit
        self.entry_price = price
        self.trades.append({'type': 'BUY', 'time': time, 'price': price})

    def sell(self, time, price):
        self.position = -1 # Simplified: 1 unit
        self.entry_price = price
        self.trades.append({'type': 'SELL', 'time': time, 'price': price})

    def close_position(self, time, price):
        pnl = (price - self.entry_price) * self.position
        self.capital += pnl
        self.trades.append({'type': 'EXIT', 'time': time, 'price': price, 'pnl': pnl})
        self.position = 0
        self.entry_price = 0

    def get_performance_report(self):
        df_trades = pd.DataFrame(self.trades)
        total_pnl = self.capital - self.initial_capital
        return {
            'final_capital': self.capital,
            'total_pnl': total_pnl,
            'total_trades': len(df_trades[df_trades['type'] == 'EXIT']),
            'trades': df_trades
        }
