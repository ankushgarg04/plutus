import sys
import os
import time
import pandas as pd
from strategy.strategy import MeanReversionMomentumStrategy
from execution.order_manager import OrderManager
from config import TRADING_PARAMS, STRATEGY_PARAMS
from utils.logger import setup_logger

# Add parent directory to path to import login
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from login import login

logger = setup_logger("live_trading")

def run_live_trading():
    api = login()
    if api is None:
        logger.error("Failed to login. Exiting.")
        return

    order_manager = OrderManager(api)
    
    # Search for Symbol Token
    symbol = TRADING_PARAMS['symbol']
    exchange = TRADING_PARAMS['exchange']
    
    logger.info(f"Searching for token: {symbol} on {exchange}")
    search_result = api.searchscrip(exchange=exchange, searchtext=symbol.split('-')[0]) # Search 'SBIN'
    
    token = None
    if search_result and 'values' in search_result:
        for scrip in search_result['values']:
             if scrip['tsym'] == symbol:
                 token = scrip['token']
                 break
    
    if not token:
        logger.error(f"Token not found for {symbol}")
        return

    logger.info(f"Starting live trading for {symbol} ({token})...")
    
    # Initialize Strategy with config params
    strategy = MeanReversionMomentumStrategy(
        momentum_period=STRATEGY_PARAMS['momentum_period'],
        rsi_period=STRATEGY_PARAMS['rsi_period'],
        rsi_oversold=STRATEGY_PARAMS['rsi_oversold'],
        rsi_overbought=STRATEGY_PARAMS['rsi_overbought']
    )
    
    while True:
        try:
            # Fetch recent data
            logger.debug("Fetching recent data...")
            end_time = time.time()
            start_time = end_time - (100 * 60) # Last 100 minutes
            
            ret = api.get_time_price_series(
                exchange=exchange, 
                token=token, 
                starttime=int(start_time), 
                endtime=int(end_time), 
                interval=TRADING_PARAMS['timeframe']
            )
            
            if ret:
                df = pd.DataFrame.from_dict(ret)
                
                # Generate signals
                df_with_signals = strategy.generate_signals(df)
                last_bar = df_with_signals.iloc[-1]
                
                logger.info(f"Time: {last_bar['time']} | Close: {last_bar['intc']} | RSI: {last_bar['rsi']:.2f} | Signal: {last_bar['signal']}")
                
                qty = TRADING_PARAMS['quantity']
                
                # Place Orders
                if last_bar['signal'] == 1:
                    logger.info(">>> BUY SIGNAL TRIGGERED")
                    order_manager.place_buy_order(symbol, qty, price=0) # Market Order
                    
                elif last_bar['signal'] == -1:
                    logger.info(">>> SELL SIGNAL TRIGGERED")
                    order_manager.place_sell_order(symbol, qty, price=0) # Market Order
                
            else:
                logger.warning("No data received from API.")
            
            # Wait for next minute
            time.sleep(60)
            
        except KeyboardInterrupt:
            logger.info("Stopping live trading (User Interrupt).")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_live_trading()
