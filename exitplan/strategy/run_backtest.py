import pandas as pd
import os
from strategy import MeanReversionMomentumStrategy
from backtesting import BacktestEngine

def run_backtest():
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '../data/SBI/sbin_data.csv')
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        return

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Initialize strategy and engine
    strategy = MeanReversionMomentumStrategy()
    engine = BacktestEngine(initial_capital=100000)
    
    # Run backtest
    print("Running backtest...")
    results = engine.run(df, strategy)
    
    # Print results
    print("\n--- Backtest Results ---")
    print(f"Final Capital: {results['final_capital']:.2f}")
    print(f"Total P&L: {results['total_pnl']:.2f}")
    print(f"Total Trades: {results['total_trades']}")
    
    if results['total_trades'] > 0:
        print("\nRecent Trades:")
        print(results['trades'].tail())

if __name__ == "__main__":
    run_backtest()
